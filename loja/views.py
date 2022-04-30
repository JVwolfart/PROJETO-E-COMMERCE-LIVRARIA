from django.shortcuts import render, redirect
from loja.models import Avaliacao, Carrinho, Categoria, DadosUser, FormaPagamento, ItemCarrinho, ItemPedido, Livro, Pedido, StatusPedido
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def index(request):
    categorias = Categoria.objects.all().order_by('categoria')
    livros = Livro.objects.all().filter(
        ativo=True
    ).order_by('-id')[:8]
    carrossel_active = Livro.objects.all().filter(
        ativo=True
    ).order_by('-avaliacao_livro', '-numero_avaliacoes').first()
    carrossel = Livro.objects.all().filter(
        ativo=True
    ).order_by('-avaliacao_livro', '-numero_avaliacoes')[1:5]
    user = request.user
    if user.is_authenticated:
        carrinho_user = Carrinho.objects.all().filter(
            usuario=user, aberto=True
        ).first()
        '''carrinho = ItemCarrinho.objects.all().filter(
            carrinho__usuario=user, carrinho__aberto=True
        ).aggregate(total=Sum('quant'))'''
        return render(request, 'index.html', {'livros':livros, 'carrossel':carrossel, 'carrossel_active':carrossel_active, 'categorias':categorias, 'carrinho_user':carrinho_user})
    else:
        return render(request, 'index.html', {'livros':livros, 'carrossel':carrossel, 'carrossel_active':carrossel_active, 'categorias':categorias})

def produto(request, id):
    categorias = Categoria.objects.all().order_by('categoria')
    livro = Livro.objects.get(id=id)
    user = request.user
    if user.is_authenticated:
        carrinho_user = Carrinho.objects.all().filter(
            usuario=user, aberto=True
        ).first()
        '''carrinho = ItemCarrinho.objects.all().filter(
            carrinho__usuario=user, carrinho__aberto=True
        ).aggregate(total=Sum('quant'))'''
        return render(request, 'produto.html', {'livro':livro, 'categorias':categorias, 'carrinho_user':carrinho_user})
    else:
        return render(request, 'produto.html', {'livro':livro, 'categorias':categorias})

def produtos(request):
    categorias = Categoria.objects.all().order_by('categoria')
    livros = Livro.objects.all().order_by('titulo').filter(
        ativo=True
    )
    paginator = Paginator(livros, 5)
    page = request.GET.get('p')
    livros = paginator.get_page(page)
    user = request.user
    if user.is_authenticated:
        carrinho_user = Carrinho.objects.all().filter(
            usuario=user, aberto=True
        ).first()
        '''carrinho = ItemCarrinho.objects.all().filter(
            carrinho__usuario=user, carrinho__aberto=True
        ).aggregate(total=Sum('quant'))'''
        return render(request, 'pesquisa.html', {'categorias':categorias, 'livros':livros, 'carrinho_user':carrinho_user})
    else:
        return render(request, 'pesquisa.html', {'categorias':categorias, 'livros':livros})

def pesquisa_termo(request):
    termo = request.GET.get('termo')
    categorias = Categoria.objects.all().order_by('categoria')
    if not termo:
        termo = ''
        livros = Livro.objects.all().filter(
            ativo=True
        ).order_by('titulo')
        paginator = Paginator(produtos, 5)
        page = request.GET.get('p')
        produtos = paginator.get_page(page)
        user = request.user
        if user.is_authenticated:
            carrinho_user = Carrinho.objects.all().filter(
                usuario=user, aberto=True
            ).first()
            '''carrinho = ItemCarrinho.objects.all().filter(
                carrinho__usuario=user, carrinho__aberto=True
            ).aggregate(total=Sum('quant'))'''
            return render(request, 'pesquisa_termo.html', {'livros':livros, 'categorias':categorias, 'termo':termo, 'carrinho_user':carrinho_user})
        else:
            return render(request, 'pesquisa_termo.html', {'livros':livros, 'categorias':categorias, 'termo':termo})
    else:
        livros = Livro.objects.all().filter(
             Q(titulo__icontains=termo) | Q(autor__autor__icontains=termo) | Q(categoria__categoria__icontains=termo), ativo=True
        ).order_by('titulo')
        paginator = Paginator(livros, 5)
        page = request.GET.get('p')
        livros = paginator.get_page(page)
        user = request.user
        if user.is_authenticated:
            carrinho_user = Carrinho.objects.all().filter(
                usuario=user, aberto=True
            ).first()
            '''carrinho = ItemCarrinho.objects.all().filter(
                carrinho__usuario=user, carrinho__aberto=True
            ).aggregate(total=Sum('quant'))'''
            return render(request, 'pesquisa_termo.html', {'livros':livros, 'categorias':categorias, 'termo':termo, 'carrinho_user':carrinho_user})
        else:
            return render(request, 'pesquisa_termo.html', {'livros':livros, 'categorias':categorias, 'termo':termo})

def categoria(request, id):
    categorias = Categoria.objects.all().order_by('categoria')
    categoria = Categoria.objects.get(id=id)
    livros = Livro.objects.all().filter(
        ativo=True, categoria=categoria
    ).order_by('-id')
    paginator = Paginator(livros, 5)
    page = request.GET.get('p')
    livros = paginator.get_page(page)
    user = request.user
    if user.is_authenticated:
        carrinho_user = Carrinho.objects.all().filter(
                usuario=user, aberto=True
        ).first()
        '''carrinho = ItemCarrinho.objects.all().filter(
            carrinho__usuario=user, carrinho__aberto=True
        ).aggregate(total=Sum('quant'))'''
        return render(request, 'categoria.html', {'categorias':categorias, 'categoria':categoria, 'livros':livros, 'carrinho_user':carrinho_user})
    else:
        return render(request, 'categoria.html', {'categorias':categorias, 'categoria':categoria, 'livros':livros})
    

def login(request):
    categorias = Categoria.objects.all().order_by('categoria')
    if request.method != 'POST':
        return render(request, 'login.html', {'categorias':categorias})
    else:
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.add_message(request, messages.ERROR, f'ERRO! Usuário ou senha inválidos')
        return render(request, 'login.html', {'categorias':categorias})
    else:
        auth.login(request, user)
        carrinho_existe = Carrinho.objects.all().filter(
            usuario=user, aberto=True
        ).exists()
        if carrinho_existe:
            carrinho_user = Carrinho.objects.all().filter(
                usuario=user, aberto=True
            ).order_by('id').first()
        else:
            carrinho_user = Carrinho.objects.create(usuario=user)
            carrinho_user.save()
        messages.add_message(request, messages.SUCCESS, f'Login feito com sucesso!')
        return redirect('home')


@login_required(login_url='login')
def alterar_senha(request):
    categorias = Categoria.objects.all().order_by('categoria')
    user = request.user
    carrinho_user = Carrinho.objects.all().filter(
        usuario=user, aberto=True
    ).first()
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, 'Senha alterada com sucesso')
            return redirect('home')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'alterar_senha.html', {'form_senha':form_senha, 'categorias':categorias, 'carrinho_user':carrinho_user})

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout feito com sucesso')
    return redirect('home')

def cadastro(request):
    categorias = Categoria.objects.all().order_by('categoria')
    if request.method != 'POST':
        return render(request, 'cadastro.html', {'categorias':categorias})
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')
    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.add_message(request, messages.ERROR, 'ERRO! nenhum campo pode ficar vazio')
        return render(request, 'cadastro.html', {'categorias':categorias})
    
    if senha != senha2:
        messages.add_message(request, messages.ERROR, 'ERRO! senhas não conferem')
        return render(request, 'cadastro.html', {'categorias':categorias})

    if len(senha) < 8:
        messages.add_message(request, messages.ERROR, 'ERRO! senha deve ter mais de 8 caracteres')
        return render(request, 'cadastro.html', {'categorias':categorias})

    if senha.isnumeric():
        messages.add_message(request, messages.ERROR, 'ERRO! senha não pode ser somente numérica')
        return render(request, 'cadastro.html', {'categorias':categorias})

    if User.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.ERROR, f'ERRO! Usuário {usuario} já existe')
        return render(request, 'cadastro.html', {'categorias':categorias})

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR, f'ERRO! Email {email} já existe')
        return render(request, 'cadastro.html')
    else:
        user = User.objects.create_user(username=usuario, email=email,  password=senha, first_name=nome, last_name=sobrenome)
        user.save()
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, f'Cadastro de {usuario} feito com sucesso, boas compras')
        return redirect('home')

@login_required(login_url='login')
def add_carrinho(request, id):
    categorias = Categoria.objects.all()
    user = request.user
    produto = Livro.objects.get(id=id)
    carrinho_aberto = Carrinho.objects.all().filter(
        usuario=user, aberto=True
    ).exists()
    
    if not carrinho_aberto:
        carrinho = Carrinho.objects.create(usuario=user)
        carrinho.save()
        carrinho_user = Carrinho.objects.all().filter(
        usuario=user, aberto=True
        ).first()#
        item = ItemCarrinho.objects.create(carrinho=carrinho_user, produto=produto, quant=1, valor_unitario=produto.preco, total_produto=produto.preco)
        item.save()
        itens = ItemCarrinho.objects.all().filter(
            carrinho=carrinho_user
        )
        n_itens = ItemCarrinho.objects.all().filter(
            carrinho=carrinho_user
        ).aggregate(n_itens=Sum('quant'))
        subtotal_carrinho = itens.aggregate(total=Sum('total_produto'))
        subtotal_carrinho = round(subtotal_carrinho['total'], 2)
        #print(subtotal_carrinho)
        carrinho_user.n_itens = n_itens['n_itens']
        carrinho_user.subtotal = subtotal_carrinho
        carrinho_user.save()
        carrinho_user.total = carrinho_user.subtotal + carrinho_user.frete
        #return render(request, 'carrinho.html', {'categorias':categorias, 'itens':itens, 'carrinho_user':carrinho_user})
        return redirect('ver_carrinho')
    else:
        carrinho_user = Carrinho.objects.all().filter(
            usuario=user, aberto=True
        ).first()#
        itens_carrinho = ItemCarrinho.objects.all().filter(
            carrinho=carrinho_user
        )
        item = itens_carrinho.filter(
            produto=produto
        ).exists()
        print(item)
        if item:
            item_existente = ItemCarrinho.objects.all().filter(
            carrinho=carrinho_user, produto=produto
            ).first()
            item_existente.quant += 1
            total = item_existente.quant * item_existente.valor_unitario
            item_existente.total_produto = total
            item_existente.save()
        else:
            item = ItemCarrinho.objects.create(carrinho=carrinho_user, produto=produto, quant=1, valor_unitario=produto.preco, total_produto=produto.preco)
            item.save()
        itens = ItemCarrinho.objects.all().filter(
            carrinho=carrinho_user
        )
        n_itens = ItemCarrinho.objects.all().filter(
            carrinho=carrinho_user
        ).aggregate(n_itens=Sum('quant'))
        carrinho_user.n_itens = n_itens['n_itens']
        subtotal_carrinho = itens.aggregate(total=Sum('total_produto'))
        subtotal_carrinho = round(subtotal_carrinho['total'], 2)
        print(subtotal_carrinho)
        carrinho_user.subtotal = subtotal_carrinho
        carrinho_user.total = carrinho_user.subtotal + carrinho_user.frete
        carrinho_user.save()
        #return render(request, 'carrinho.html', {'categorias':categorias, 'itens':itens, 'carrinho_user':carrinho_user})
        return redirect('ver_carrinho')


@login_required(login_url='login')
def ver_carrinho(request):
    categorias = Categoria.objects.all()
    user = request.user
    carrinho_user = Carrinho.objects.all().filter(
        usuario=user, aberto=True
    ).first()
    if not carrinho_user:
        carrinho_user = Carrinho.objects.create(usuario=user)
        carrinho_user.save()
    itens = ItemCarrinho.objects.all().filter(
        carrinho=carrinho_user
    )
    '''carrinho = ItemCarrinho.objects.all().filter(
        carrinho__usuario=user, carrinho__aberto=True
    ).aggregate(total=Sum('quant'))'''
    if carrinho_user.n_itens == 0:
        messages.add_message(request, messages.WARNING, 'Seu carrinho está vazio, adicione algum item e boas compras!!!')
    return render(request, 'carrinho.html', {'categorias':categorias, 'carrinho_user':carrinho_user, 'itens':itens})

@login_required(login_url='login')
def add_item_carrinho(request, id):
    item = ItemCarrinho.objects.get(id=id)
    estoque = item.produto.estoque
    if estoque > item.quant:
        id_carrinho = item.carrinho.id
        item.quant += 1
        item.total_produto = item.quant * item.valor_unitario
        item.save()
        carrinho = Carrinho.objects.get(
            id=id_carrinho
        )
        itens = ItemCarrinho.objects.all().filter(
            carrinho=carrinho
        ).aggregate(subtotal=Sum('total_produto'))
        n_itens = ItemCarrinho.objects.all().filter(
            carrinho=carrinho
        ).aggregate(n_itens=Sum('quant'))
        carrinho.subtotal = itens['subtotal']
        carrinho.total = carrinho.subtotal
        carrinho.n_itens = n_itens['n_itens']
        carrinho.frete = 0
        carrinho.save()
        return redirect('ver_carrinho')
    else:
        messages.add_message(request, messages.WARNING, f'O produto {item.produto} possui apenas em seu estoque {estoque} unidades e portanto não foi possível adicionar mais itens desse produto, lamento')
        return redirect('ver_carrinho')

@login_required(login_url='login')
def excluir_item_carrinho(request, id):
    item = ItemCarrinho.objects.get(id=id)
    id_carrinho = item.carrinho.id
    item.quant -= 1
    item.total_produto = item.quant * item.valor_unitario
    carrinho = Carrinho.objects.get(
        id=id_carrinho
    )
    if item.quant > 0:
        item.save()
        itens = ItemCarrinho.objects.all().filter(
            carrinho=carrinho
            ).aggregate(subtotal=Sum('total_produto'))
        n_itens = ItemCarrinho.objects.all().filter(
            carrinho=carrinho
            ).aggregate(n_itens=Sum('quant'))
        carrinho.subtotal = itens['subtotal']
        carrinho.total = carrinho.subtotal
        carrinho.n_itens = n_itens['n_itens']
        carrinho.frete = 0
        carrinho.save()
    else:
        item.delete()
        #carrinho.n_itens = 0
        '''sobrou_item = ItemCarrinho.objects.all().filter(
            carrinho=carrinho
        ).exists()'''
        if carrinho.n_itens > 0:
            itens = ItemCarrinho.objects.all().filter(
                carrinho=carrinho
            ).aggregate(subtotal=Sum('total_produto'))
            n_itens = ItemCarrinho.objects.all().filter(
                carrinho=carrinho
            ).aggregate(n_itens=Sum('quant'))
            if not itens['subtotal']:
                itens['subtotal'] = 0
            if not n_itens['n_itens']:
                n_itens['n_itens'] = 0
            print(itens['subtotal'])
            carrinho.subtotal = itens['subtotal']
            carrinho.total = carrinho.subtotal
            carrinho.n_itens = n_itens['n_itens']
            carrinho.frete = 0
            carrinho.save()
        else:
            carrinho.subtotal = 0
            carrinho.total = 0
            carrinho.n_itens = 0
            carrinho.frete = 0
            carrinho.save()
    return redirect('ver_carrinho')

@login_required(login_url='login')
def calcular_frete(request, id):
    carrinho_user = Carrinho.objects.get(id=id)
    frete = float(carrinho_user.n_itens) * 4.99
    frete = round(frete, 2)
    if frete > 50:
        carrinho_user.frete = frete
        carrinho_user.frete_gratis = True
        carrinho_user.total = float(carrinho_user.subtotal)
        carrinho_user.save()
    else:    
        carrinho_user.frete = frete
        carrinho_user.frete_gratis = False
        carrinho_user.total = float(carrinho_user.subtotal) + frete
        carrinho_user.save()
    return redirect('ver_carrinho')

@login_required(login_url='login')
def selecionar_endereco(request, id):
    categorias = Categoria.objects.all().order_by('categoria')
    fpags = FormaPagamento.objects.all()
    carrinho_user = Carrinho.objects.get(id=id)
    user = request.user
    endereco = DadosUser.objects.all().filter(
        usuario=user
    ).exists()
    itens = ItemCarrinho.objects.all().filter(
        carrinho=carrinho_user
    )
    if carrinho_user.frete == 0:
        messages.add_message(request, messages.WARNING, 'Atualize o valor do frete para prosseguir')
        return redirect('ver_carrinho')
    if not endereco:
        return redirect('cadastrar_endereco')
    else:
        enderecos = DadosUser.objects.all().filter(
            usuario=user
        )
        return render(request, 'selecionar_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user, 'enderecos':enderecos, 'itens':itens, 'fpags':fpags})

@login_required(login_url='login')
def cadastrar_endereco(request):
    categorias = Categoria.objects.all().order_by('categoria')
    user = request.user
    carrinho_user = Carrinho.objects.all().filter(
        usuario=user, aberto=True
    ).first()
    if request.method != 'POST':
        return render(request, 'cadastro_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user})
    else:
        nome = request.POST.get('nome').strip().title()
        rua = request.POST.get('rua').strip().title()
        bairro = request.POST.get('bairro').strip().title()
        cidade = request.POST.get('cidade').strip().title()
        estado = request.POST.get('estado')
        numero = request.POST.get('numero').strip()
        complemento = request.POST.get('complemento').strip().title()
        cep = request.POST.get('cep').strip()
        ddd = request.POST.get('ddd').strip()
        telefone = request.POST.get('telefone').strip()
        if not nome or not rua or not bairro or not cidade or not estado or not numero or not cep or not telefone or not ddd:
            messages.add_message(request, messages.ERROR, 'Nenhum campo pode ficar vazio, verifique')
            return render(request, 'cadastro_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user})
        if not ddd.isnumeric() or len(ddd) != 2:
            messages.add_message(request, messages.ERROR, 'DDD deve ser un valor numérico composto por 2 algarismos')
            return render(request, 'cadastro_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user})
        if not telefone.isnumeric() or len(telefone) < 8:
            messages.add_message(request, messages.ERROR, 'Telefone deve ser composto por pelo menos 8 algarismos')
            return render(request, 'cadastro_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user})
        telefone = '(' + ddd + ')' + telefone
        if not cep.isnumeric() or len(cep) != 8:
            messages.add_message(request, messages.ERROR, 'CEP deve ser composto por 8 algarismos, digite apenas os números, sem pontos ou traços')
            return render(request, 'cadastro_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user})
        cep = cep[0:2] + '.' + cep[2:5] + '-' + cep[5:]
        endereco = DadosUser.objects.create(usuario=user, nome=nome, rua=rua, bairro=bairro, municipio=cidade, estado=estado, complemento=complemento, numero=numero, cep=cep, telefone=telefone)
        endereco.save()
        messages.add_message(request, messages.SUCCESS, 'Novo endereço adicionado com sucesso')
        return redirect('selecionar_endereco', carrinho_user.id)

@login_required(login_url='login')
def add_endereco(request):
    categorias = Categoria.objects.all().order_by('categoria')
    user = request.user
    carrinho_user = Carrinho.objects.all().filter(
        usuario=user, aberto=True
    ).first()
    if request.method != 'POST':
        return render(request, 'cadastro_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user})
    else:
        nome = request.POST.get('nome').strip().title()
        rua = request.POST.get('rua').strip().title()
        bairro = request.POST.get('bairro').strip().title()
        cidade = request.POST.get('cidade').strip().title()
        estado = request.POST.get('estado')
        numero = request.POST.get('numero').strip()
        complemento = request.POST.get('complemento').strip().title()
        cep = request.POST.get('cep').strip()
        ddd = request.POST.get('ddd').strip()
        telefone = request.POST.get('telefone').strip()
        if not nome or not rua or not bairro or not cidade or not estado or not numero or not cep or not telefone or not ddd:
            messages.add_message(request, messages.ERROR, 'Nenhum campo pode ficar vazio, verifique')
            return render(request, 'cadastro_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user})
        if not ddd.isnumeric() or len(ddd) != 2:
            messages.add_message(request, messages.ERROR, 'DDD deve ser un valor numérico composto por 2 algarismos')
            return render(request, 'cadastro_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user})
        if not telefone.isnumeric() or len(telefone) < 8:
            messages.add_message(request, messages.ERROR, 'Telefone deve ser composto por pelo menos 8 algarismos')
            return render(request, 'cadastro_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user})
        telefone = '(' + ddd + ')' + telefone
        if not cep.isnumeric() or len(cep) != 8:
            messages.add_message(request, messages.ERROR, 'CEP deve ser composto por 8 algarismos, digite apenas os números, sem pontos ou traços')
            return render(request, 'cadastro_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user})
        cep = cep[0:2] + '.' + cep[2:5] + '-' + cep[5:]
        endereco = DadosUser.objects.create(usuario=user, nome=nome, rua=rua, bairro=bairro, municipio=cidade, estado=estado, complemento=complemento, numero=numero, cep=cep, telefone=telefone)
        endereco.save()
        messages.add_message(request, messages.SUCCESS, 'Novo endereço adicionado com sucesso')
        return redirect('meus_dados')

@login_required(login_url='login')
def alterar_endereco(request, id):
    categorias = Categoria.objects.all().order_by('categoria')
    user = request.user
    carrinho_user = Carrinho.objects.all().filter(
        usuario=user, aberto=True
    ).first()
    endereco = DadosUser.objects.get(id=id)
    retorno_cep = endereco.cep.replace('.','').replace('-', '')
    retorno_ddd = endereco.telefone[1:3]
    retorno_telefone = endereco.telefone[4:]
    retorno = {'cep':retorno_cep, 'ddd':retorno_ddd, 'telefone':retorno_telefone}
    if request.method != 'POST':
        return render(request, 'alterar_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user, 'endereco':endereco, 'retorno':retorno})
    else:
        
        nome = request.POST.get('nome').strip().title()
        rua = request.POST.get('rua').strip().title()
        bairro = request.POST.get('bairro').strip().title()
        cidade = request.POST.get('cidade').strip().title()
        estado = request.POST.get('estado')
        numero = request.POST.get('numero').strip()
        complemento = request.POST.get('complemento').strip().title()
        cep = request.POST.get('cep').strip()
        ddd = request.POST.get('ddd').strip()
        telefone = request.POST.get('telefone').strip()
        if not nome or not rua or not bairro or not cidade or not estado or not numero or not cep or not telefone or not ddd:
            messages.add_message(request, messages.ERROR, 'Nenhum campo pode ficar vazio, verifique')
            return render(request, 'alterar_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user, 'endereco':endereco, 'retorno':retorno})
        if len(estado) != 2:
            messages.add_message(request, messages.ERROR, 'Selecione um estado válido')
            return render(request, 'alterar_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user, 'endereco':endereco, 'retorno':retorno})
        if not ddd.isnumeric() or len(ddd) != 2:
            messages.add_message(request, messages.ERROR, 'DDD deve ser un valor numérico composto por 2 algarismos')
            return render(request, 'alterar_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user, 'endereco':endereco, 'retorno':retorno})
        if not telefone.isnumeric() or len(telefone) < 8:
            messages.add_message(request, messages.ERROR, 'Telefone deve ser composto por pelo menos 8 algarismos')
            return render(request, 'alterar_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user, 'endereco':endereco, 'retorno':retorno})
        telefone = '(' + ddd + ')' + telefone
        if not cep.isnumeric() or len(cep) != 8:
            messages.add_message(request, messages.ERROR, 'CEP deve ser composto por 8 algarismos, digite apenas os números, sem pontos ou traços')
            return render(request, 'alterar_endereco.html', {'categorias':categorias, 'carrinho_user':carrinho_user, 'endereco':endereco, 'retorno':retorno})
        cep = cep[0:2] + '.' + cep[2:5] + '-' + cep[5:]
        endereco.nome = nome
        endereco.bairro = bairro
        endereco.rua = rua
        endereco.numero = numero
        endereco.complemento = complemento
        endereco.cep = cep
        endereco.cidade = cidade
        endereco.estado = estado
        endereco.telefone = telefone
        endereco.save()
        messages.add_message(request, messages.SUCCESS, 'Endereço alterado com sucesso')
        return redirect('meus_dados')

@login_required(login_url='login')
def entrega(request):
    categorias = Categoria.objects.all().order_by('categoria')
    user = request.user
    carrinho_user = Carrinho.objects.all().filter(
        usuario=user, aberto=True
    ).first()
    if request.method != 'POST':
        return redirect('selecionar_endereco', carrinho_user.id)
    else:
        ender = request.POST.get('endereco')
        fpag = request.POST.get('forma')
        if not ender or not fpag:
            messages.add_message(request, messages.ERROR, 'Selecione um endereço para receber o produto ou cadastre um novo endereço e também uma forma de pagamento')
            return redirect('selecionar_endereco', carrinho_user.id)
        else:
            endereco = DadosUser.objects.get(id=ender)
            forma = FormaPagamento.objects.get(id=fpag)
            itens = ItemCarrinho.objects.all().filter(
                carrinho=carrinho_user
            )
            for item in itens:
                if item.quant > item.produto.estoque:
                    messages.add_message(request, messages.ERROR, f'O item {item.produto} possui apenas {item.produto.estoque} unidades, por favor atualize seu carrinho antes de finalizar')
                    return redirect('ver_carrinho')
                
            carrinho_user.entrega = endereco
            carrinho_user.forma_pagamento = forma
            carrinho_user.save()
            return render(request, 'finalizar_pedido.html', {'categorias':categorias, 'carrinho_user':carrinho_user, 'itens':itens})

@login_required(login_url='login')
def finalizar_pedido(request):
    categorias = Categoria.objects.all().order_by('categoria')
    user = request.user
    carrinho_user = Carrinho.objects.all().filter(
        usuario=user, aberto=True
    ).first()
    itens = ItemCarrinho.objects.all().filter(
        carrinho=carrinho_user
    )
    fpags = FormaPagamento.objects.all()
    status_pedido = StatusPedido.objects.all()
    pedido_criado = StatusPedido.objects.get(status='Pedido criado')
    livros = Livro.objects.all()
    subtotal = carrinho_user.subtotal
    frete = carrinho_user.frete
    frete_gratis = carrinho_user.frete_gratis
    total = carrinho_user.total
    n_itens = carrinho_user.n_itens
    entrega = carrinho_user.entrega
    forma_pagamento = carrinho_user.forma_pagamento
    novo_pedido = Pedido.objects.create(usuario=user, situacao=pedido_criado, subtotal=subtotal, frete=frete, frete_gratis=frete_gratis, total=total, n_itens=n_itens, entrega=entrega, forma_pagamento=forma_pagamento)
    novo_pedido.save()
    pedido_cliente = Pedido.objects.all().filter(
        situacao=pedido_criado, usuario=user
    ).first()
    for i in itens:
        produto = i.produto
        quant = i.quant
        valor_unitario = i.valor_unitario
        total_produto = i.total_produto
        item_pedido = ItemPedido.objects.create(pedido=pedido_cliente, produto=produto, quant=quant, valor_unitario=valor_unitario, total_produto=total_produto)
        livro = Livro.objects.get(id=i.produto.id)
        livro.estoque -= i.quant
        livro.quantidades_vendidas += i.quant
        livro.save()
        item_pedido.save()
    carrinho_user.aberto = False
    aguardando_pagamento = StatusPedido.objects.get(status='Aguardando pagamento')
    pedido_cliente.situacao = aguardando_pagamento
    pedido_cliente.save()
    carrinho_user.save()
    messages.add_message(request, messages.SUCCESS, f'Pedido {pedido_cliente} criado e aguardando pagamento')
    return redirect('home')

@login_required(login_url='login')
def meus_pedidos(request):
    categorias = Categoria.objects.all().order_by('categoria')
    user = request.user
    carrinho_user = Carrinho.objects.all().filter(
        usuario=user, aberto=True
    ).first()
    pedidos = Pedido.objects.all().filter(
        usuario=user
    ).order_by('-id')
    return render(request, 'meus_pedidos.html', {'categorias':categorias, 'carrinho_user':carrinho_user, 'pedidos':pedidos})

@login_required(login_url='login')
def itens_pedido(request, id):
    categorias = Categoria.objects.all().order_by('categoria')
    user = request.user
    carrinho_user = Carrinho.objects.all().filter(
        usuario=user, aberto=True
    ).first()
    pedido = Pedido.objects.get(id=id)
    itens = ItemPedido.objects.all().filter(
        pedido=pedido
    )
    return render(request, 'itens_pedido.html', {'categorias':categorias, 'carrinho_user':carrinho_user, 'pedido':pedido, 'itens':itens})

@login_required(login_url='login')
def meus_dados(request):
    categorias = Categoria.objects.all().order_by('categoria')
    user = request.user
    carrinho_user = Carrinho.objects.all().filter(
        usuario=user, aberto=True
    ).first()
    enderecos = DadosUser.objects.all().filter(
        usuario=user
    )
    return render(request, 'meus_dados.html', {'categorias':categorias, 'carrinho_user':carrinho_user, 'enderecos':enderecos})

def avaliacao(request, id):
    categorias = Categoria.objects.all().order_by('categoria')
    user = request.user
    livro = Livro.objects.get(id=id)
    
    if request.method != 'POST':
        if user.is_authenticated:
            carrinho_user = Carrinho.objects.all().filter(
                usuario=user, aberto=True
            ).first()
            return render(request, 'avaliacao.html', {'livro':livro, 'categorias':categorias, 'carrinho_user':carrinho_user})
        else:
            return render(request, 'avaliacao.html', {'livro':livro, 'categorias':categorias})
    else:
        nome = request.POST.get('nome')
        comentario = request.POST.get('comentario').strip()
        avaliacao = request.POST.get('estrela')
        if not nome:
            nome = 'Anônimo'
        if not avaliacao:
            if user.is_authenticated:
                carrinho_user = Carrinho.objects.all().filter(
                    usuario=user, aberto=True
                ).first()
                messages.add_message(request, messages.ERROR, 'Selecione a nota do livro')
                return render(request, 'avaliacao.html', {'livro':livro, 'categorias':categorias, 'carrinho_user':carrinho_user})
            else:
                messages.add_message(request, messages.ERROR, 'Selecione a nota do livro')
                return render(request, 'avaliacao.html', {'livro':livro, 'categorias':categorias})
        else:
            avaliacao = int(avaliacao)
            if user.is_authenticated:
                nota = Avaliacao.objects.create(usuario=user, nome=nome, comentario=comentario, livro=livro, nota=avaliacao)

            else:
                nota = Avaliacao.objects.create(nome=nome, comentario=comentario, livro=livro, nota=avaliacao)
            nota.save()
            avaliacoes = Avaliacao.objects.all().filter(
                livro=livro
            ).aggregate(media=Avg('nota'))
            livro.numero_avaliacoes += 1
            livro.avaliacao_livro = avaliacoes['media']
            livro.save()
            messages.add_message(request, messages.SUCCESS, 'Avaliação registrada com sucesso')
            return redirect('produto', livro.id)

def ver_avaliacoes(request, id):
    categorias = Categoria.objects.all().order_by('categoria')
    user = request.user
    livro = Livro.objects.get(id=id)
    avaliacoes = Avaliacao.objects.all().filter(
        livro=livro
    ).order_by('nota')
    paginator = Paginator(avaliacoes, 5)
    page = request.GET.get('p')
    avaliacoes = paginator.get_page(page)
    if user.is_authenticated:
            carrinho_user = Carrinho.objects.all().filter(
                usuario=user, aberto=True
            ).first()
            return render(request, 'ver_avaliacoes.html', {'livro':livro, 'categorias':categorias, 'carrinho_user':carrinho_user, 'avaliacoes':avaliacoes})
    else:
        return render(request, 'ver_avaliacoes.html', {'livro':livro, 'categorias':categorias, 'avaliacoes':avaliacoes})

@login_required(login_url='login')
def deixar_pra_depois(request):
    categorias = Categoria.objects.all().order_by('categoria')
    user = request.user
    carrinho_user = Carrinho.objects.all().filter(
        usuario=user, aberto=True
    ).first()
    carrinho_user.frete = 0
    carrinho_user.frete_gratis = False
    carrinho_user.total = carrinho_user.subtotal
    carrinho_user.save()
    return redirect('home')