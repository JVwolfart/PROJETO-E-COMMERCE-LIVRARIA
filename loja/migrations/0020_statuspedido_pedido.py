# Generated by Django 4.0.3 on 2022-04-28 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loja', '0019_formapagamento_carrinho_forma_pagamento'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('frete', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, null=True)),
                ('frete_gratis', models.BooleanField(default=False)),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('n_itens', models.IntegerField(default=0)),
                ('entrega', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='loja.dadosuser')),
                ('forma_pagamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='loja.formapagamento')),
                ('situacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='loja.statuspedido')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
