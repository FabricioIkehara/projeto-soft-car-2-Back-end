# Generated by Django 5.1.5 on 2025-05-02 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_order_register', '0002_order_servicos_order_valor_total_alter_order_carro_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
