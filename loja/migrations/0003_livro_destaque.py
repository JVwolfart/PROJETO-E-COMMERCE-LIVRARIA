# Generated by Django 4.0.3 on 2022-04-26 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0002_avaliacao_comentario_livro_sinopse'),
    ]

    operations = [
        migrations.AddField(
            model_name='livro',
            name='destaque',
            field=models.BooleanField(default=False),
        ),
    ]
