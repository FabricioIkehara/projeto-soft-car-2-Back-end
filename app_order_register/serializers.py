from rest_framework import serializers # type: ignore
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'client', 'telefone', 'carro', 'cor', 'placa', 'email', 'observacoes','status']
