from django.contrib import admin
from .models import Categoria, Autor, FormaPagamento, ItemPedido, Livro, DadosUser, Carrinho, ItemCarrinho, Avaliacao, Pedido, StatusPedido
# Register your models here.

class AdmLivro(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'categoria', 'autor', 'estoque', 'preco', 'avaliacao_livro', 'numero_avaliacoes')
    list_display_links = ('id', 'titulo',)
    list_per_page = 10
    search_field = ['titulo',]
    list_filter = ['categoria']
    list_editable = ('avaliacao_livro', 'numero_avaliacoes')


admin.site.register(Categoria)
admin.site.register(FormaPagamento)
admin.site.register(StatusPedido)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
admin.site.register(Autor)
admin.site.register(Livro, AdmLivro)
admin.site.register(DadosUser)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)
admin.site.register(Avaliacao)