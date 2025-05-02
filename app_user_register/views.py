from django.http import Http404, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from .models import FormEntry
from .serializers import FormEntrySerializer
from .models import FormEntry
import json

@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("JSON recebido:", data)
            required_fields = ['client', 'telefone', 'carro', 'cor', 'placa', 'email']
            if not all(field in data and data[field] for field in required_fields):
                return HttpResponseBadRequest("Campos obrigatórios ausentes.")
            FormEntry.objects.create(
                client=data['client'],
                telefone=data['telefone'],
                carro=data['carro'],
                cor=data['cor'],
                placa=data['placa'],
                email=data['email'],
                observacao=data.get('observacao', '')
            )
            return JsonResponse({'message': 'Dados inseridos com sucesso!'}, status=201)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("JSON malformado.")
        except KeyError as e:
            return HttpResponseBadRequest(f"Campo ausente: {str(e)}")
    return HttpResponseBadRequest("Método não permitido.")

def getClientById(request, id):
    try:
        client = FormEntry.objects.get(id=id)
        data = {
            'client': client.client,
            'telefone': client.telefone,
            'carro': client.carro,
            'cor': client.cor,
            'email': client.email,
            'placa': client.placa,
            'observacao': client.observacao,
        }
        return JsonResponse(data, safe=False)
    except FormEntry.DoesNotExist:
        return JsonResponse({'error': 'Client not found'}, status=404)

class ClientListView(APIView):
    def get(self, request):
        clients = FormEntry.objects.all().order_by('-id')
        serializer = FormEntrySerializer(clients, many=True)
        return Response(serializer.data)
