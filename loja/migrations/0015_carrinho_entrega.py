# Generated by Django 4.0.3 on 2022-04-28 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0014_dadosuser_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrinho',
            name='entrega',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='loja.dadosuser'),
        ),
    ]
