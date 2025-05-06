# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Produto, CarrinhoItem, Venda
from django.contrib.auth import logout
from django.contrib import messages  
from django.contrib.auth.decorators import login_required


from .models import CarrinhoItem


def home(request):
    return render(request, 'vendas/home.html')


def produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'vendas/produtos.html', {'produtos': produtos})


def produto_detalhe(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    return render(request, 'vendas/produto_detalhe.html', {'produto': produto})


@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    quantidade_str = request.POST.get('quantidade')
    quantidade = int(quantidade_str) if quantidade_str and quantidade_str.isdigit() else 1

    carrinho_item, criado = CarrinhoItem.objects.get_or_create(
        user=request.user,
        produto=produto
    )

    if not criado:
        carrinho_item.quantidade += quantidade
    else:
        carrinho_item.quantidade = quantidade

    carrinho_item.save()
    return redirect('carrinho')


@login_required
def carrinho(request):
    carrinho_items = CarrinhoItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in carrinho_items)
    return render(request, 'vendas/carrinho.html', {'carrinho_items': carrinho_items, 'total': total})

@login_required
def remover_uma_unidade(request, item_id):
    try:
        item = CarrinhoItem.objects.get(id=item_id, user=request.user)
    except CarrinhoItem.DoesNotExist:
        return redirect('carrinho')

    if item.quantidade > 1:
        item.quantidade -= 1
        item.save()
    else:
        item.delete()

    return redirect('carrinho')



    return redirect('carrinho')
@login_required
def remover_do_carrinho(request, produto_id):
    item = CarrinhoItem.objects.filter(user=request.user, produto__id=produto_id).first()
    if item:
        item.delete()
    return redirect('carrinho')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'vendas/login.html', {'erro': 'Usuário ou senha inválidos'})
    return render(request, 'vendas/login.html')



def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'vendas/cadastro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já está em uso.")
            return render(request, 'vendas/cadastro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Já existe uma conta com este e-mail.")
            return render(request, 'vendas/cadastro.html')

        User.objects.create_user(username=username, email=email, password=password1)
        return redirect('/login/')

    return render(request, 'vendas/cadastro.html')


def logout_view(request):
    logout(request)
    return redirect('home')  


def finalizar_venda(request):
    carrinho_items = CarrinhoItem.objects.filter(user=request.user)

    if not carrinho_items.exists():
        return redirect('carrinho') 

    for item in carrinho_items:
        
        Venda.objects.create(
            user=request.user,
            produto=item.produto,
            quantidade=item.quantidade
        )

        
        item.produto.quantidade -= item.quantidade
        item.produto.save()


    carrinho_items.delete()

    return render(request, 'vendas/finalizar_venda.html')



def historico_vendas(request):
    vendas = Venda.objects.filter(user=request.user).order_by('-data')
    return render(request, 'vendas/historico.html', {'vendas': vendas})

def cancelar_carrinho(request):
    CarrinhoItem.objects.filter(user=request.user).delete()
    return redirect('produtos')