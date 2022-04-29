from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Categoria(models.Model):
    categoria = models.CharField(max_length=30)
    def __str__(self):
        return self.categoria

class Autor(models.Model):
    autor = models.CharField(max_length=100)
    def __str__(self):
        return self.autor

class DadosUser(models.Model):
    nome = models.CharField(max_length=20, blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    rua = models.CharField(max_length=150)
    bairro = models.CharField(max_length=80)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(blank=True, null=True, max_length=150)
    cep = models.CharField(max_length=20)
    telefone = models.CharField(max_length=20)
    municipio = models.CharField(max_length=80)
    estado = models.CharField(max_length=2)
    def __str__(self):
        return f'{self.nome} do {self.usuario}'

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.DO_NOTHING)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    estoque = models.IntegerField()
    preco = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    capa = models.ImageField(upload_to='fotos/capas')
    avaliacao_livro = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    numero_avaliacoes = models.IntegerField(default=0)
    excerto = models.TextField(blank=True, null=True, max_length=200)
    sinopse = models.TextField(blank=True, null=True)
    destaque = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    quantidades_vendidas = models.IntegerField(blank=True, null=True, default=0)
    def __str__(self):
        return self.titulo

class Avaliacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    nome = models.CharField(max_length=255, default='Anônimo')
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    nota = models.IntegerField(blank=True, null=True, choices=((1, '1 estrela',), (2, '2 estrelas',), (3, '3 estrelas',), (4, '4 estrelas',), (5, '5 estrelas',),))
    comentario = models.TextField(blank=True, null=True)
    def __str__(self):
        return f'Avaliação de {self.nome}'

class FormaPagamento(models.Model):
    forma = models.CharField(max_length=50)
    def __str__(self):
        return self.forma

class Carrinho(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    frete = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, default=0)
    frete_gratis = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    n_itens = models.IntegerField(default=0)
    entrega = models.ForeignKey(DadosUser, on_delete=models.DO_NOTHING, blank=True, null=True)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.DO_NOTHING, blank=True, null=True)
    aberto = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Carrinho de {self.usuario}'

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    produto = models.ForeignKey(Livro, on_delete=models.DO_NOTHING)
    quant = models.IntegerField(blank=True, null=True)
    valor_unitario = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    total_produto = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f'O {self.carrinho} adicionou {self.produto}'

class StatusPedido(models.Model):
    status = models.CharField(max_length=50)
    def __str__(self):
        return self.status

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    frete = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True, default=0)
    frete_gratis = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    n_itens = models.IntegerField(default=0)
    entrega = models.ForeignKey(DadosUser, on_delete=models.DO_NOTHING, blank=True, null=True)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.DO_NOTHING, blank=True, null=True)
    situacao = models.ForeignKey(StatusPedido, on_delete=models.DO_NOTHING, blank=True, null=True)
    data = models.DateField(default=timezone.now)
    def __str__(self):
        return f'Pedido N° {self.id}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Livro, on_delete=models.DO_NOTHING)
    quant = models.IntegerField(blank=True, null=True)
    valor_unitario = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    total_produto = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    def __str__(self):
        return f'O {self.pedido} adicionou {self.produto}'