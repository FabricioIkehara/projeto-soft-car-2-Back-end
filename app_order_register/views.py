from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Order
import json

@method_decorator(csrf_exempt, name='dispatch')
class SubmitOrderView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Carregar o corpo do request como JSON
            data = json.loads(request.body)
            print("JSON recebido:", data)

            # Verificar se os campos obrigatórios estão presentes
            required_fields = ['client', 'telefone', 'carro', 'cor', 'placa', 'servicos', 'valorTotal']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]

            if missing_fields:
                return JsonResponse(
                    {'error': f'Campos obrigatórios ausentes ou vazios: {", ".join(missing_fields)}'},
                    status=400
                )

            # Criar a instância de Order com os dados recebidos
            order = Order.objects.create(
                client=data['client'],
                telefone=data['telefone'],
                carro=data['carro'],
                cor=data['cor'],
                placa=data['placa'],
                email=data['email'],
                status=data.get('status', 'Pendente'),  # Campo opcional com valor padrão
                observacao=data.get("observacao", ""),  # Campo opcional
                servicos=data['servicos'],  # Recebido como JSON
                valor_total=data['valorTotal']
            )

            return JsonResponse({'message': 'Pedido adicionado com sucesso!', 'order_id': order.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON malformado.'}, status=400)

        except KeyError as e:
            return JsonResponse({'error': f'Campo ausente: {str(e)}'}, status=400)

        except Exception as e:
            print(f"Erro inesperado: {e}")
            return JsonResponse({'error': 'Erro ao salvar pedido.'}, status=500)

@csrf_exempt
def get_orders(request):
    if request.method == 'GET':
        try:
            # Buscar todos os pedidos e retornar como lista de dicionários
            orders = list(Order.objects.values())
            return JsonResponse(orders, safe=False, status=200)

        except Exception as e:
            print(f"Erro ao buscar pedidos: {e}")
            return JsonResponse({'error': 'Erro ao buscar pedidos.'}, status=500)

    return HttpResponseBadRequest("Método não permitido.")
