# Generated by Django 4.0.3 on 2022-04-28 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0021_itempedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='livro',
            name='quantidades_vendidas',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
