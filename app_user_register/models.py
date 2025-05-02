# app_user_register/models.py
from django.db import models

class FormEntry(models.Model):
    client = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    carro = models.CharField(max_length=255)
    cor = models.CharField(max_length=100)
    placa = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.client

