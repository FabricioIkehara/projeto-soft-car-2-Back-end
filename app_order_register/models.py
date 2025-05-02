from django.db import models

class Order(models.Model):
    client = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    carro = models.CharField(max_length=50)
    cor = models.CharField(max_length=30)
    placa = models.CharField(max_length=10)
    email = models.CharField(max_length=30)
    status = models.CharField(max_length=20, default='Pendente')
    observacao = models.TextField(blank=True, null=True)
    servicos = models.JSONField(default=list) 
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  


    def __str__(self):
        return f"Order {self.id} - {self.client}"
