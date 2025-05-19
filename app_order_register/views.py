from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Order
import json
import requests # type: ignore

# Função existente para enviar e-mail via Brevo
def send_email_via_brevo(to_email, client_name, pedido_id):
    url = "https://api.brevo.com/v3/smtp/email"
    api_key = "qAvyxXI2cOUk0gCj"  # Substitua por sua chave Brevo (mova para settings.py)
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    data = {
        "sender": {"name": "Sua Empresa", "email": "seu@email.com"},
        "to": [{"email": to_email}],
        "subject": "Seu pedido está pronto!",
        "htmlContent": f"<h3>Olá, {client_name}!</h3><p>Seu pedido #{pedido_id} está pronto para retirada!</p>"
    }

    response = requests.post(url, json=data, headers=headers)
    return response.status_code == 201

# Função existente para verificar e enviar e-mail
def check_and_send_email(order):
    if order.status.lower() == 'pronto':
        email_enviado = send_email_via_brevo(order.email, order.client, order.id)
        if not email_enviado:
            print(f"Erro ao enviar email para {order.email}")
        return email_enviado
    return False

# View existente para criar pedidos
@method_decorator(csrf_exempt, name='dispatch')
class SubmitOrderView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            print("JSON recebido:", data)

            required_fields = ['client', 'telefone', 'carro', 'cor', 'placa', 'servicos', 'valorTotal']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]

            if missing_fields:
                return JsonResponse(
                    {'error': f'Campos obrigatórios ausentes ou vazios: {", ".join(missing_fields)}'},
                    status=400
                )

            order = Order.objects.create(
                client=data['client'],
                telefone=data['telefone'],
                carro=data['carro'],
                cor=data['cor'],
                placa=data['placa'],
                email=data['email'],
                status=data.get('status', 'Pendente'),
                observacao=data.get("observacao", ""),
                servicos=data['servicos'],
                valor_total=data['valorTotal']
            )

            if order.status.lower() == 'pronto':
                check_and_send_email(order)

            return JsonResponse({'message': 'Pedido adicionado com sucesso!', 'order_id': order.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON malformado.'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Campo ausente: {str(e)}'}, status=400)
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return JsonResponse({'error': 'Erro ao salvar pedido.'}, status=500)

# View existente para listar pedidos
@csrf_exempt
def get_orders(request):
    if request.method == 'GET':
        try:
            orders = list(Order.objects.values())
            return JsonResponse(orders, safe=False, status=200)
        except Exception as e:
            print(f"Erro ao buscar pedidos: {e}")
            return JsonResponse({'error': 'Erro ao buscar pedidos.'}, status=500)
    return HttpResponseBadRequest("Método não permitido.")

# Nova view para enviar e-mail de confirmação
@method_decorator(csrf_exempt, name='dispatch')
class SendEmailView(View):
    def post(self, request, id):
        try:
            try:
                order = Order.objects.get(id=id)
            except Order.DoesNotExist:
                return JsonResponse({'error': 'Pedido não encontrado.'}, status=404)

            # Verificar se o status é "Concluído" (opcional, já validado no frontend)
            if order.status.lower() != 'concluído':
                return JsonResponse({'error': 'O pedido não está concluído.'}, status=400)

            # Enviar e-mail usando a função existente
            email_enviado = send_email_via_brevo(order.email, order.client, order.id)
            if email_enviado:
                return JsonResponse({'message': 'E-mail de confirmação enviado com sucesso!'}, status=200)
            else:
                return JsonResponse({'error': 'Erro ao enviar e-mail.'}, status=500)

        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            return JsonResponse({'error': 'Erro ao processar envio de e-mail.'}, status=500)