# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Produto, CarrinhoItem


def home(request):
    return render(request, 'vendas/home.html')


def produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'vendas/produtos.html', {'produtos': produtos})


def produto_detalhe(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    return render(request, 'vendas/produto_detalhe.html', {'produto': produto})


def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if produto.quantidade > 0:
        item, criado = CarrinhoItem.objects.get_or_create(user=request.user, produto=produto)
        item.quantidade += 1
        item.save()
        produto.quantidade -= 1
        produto.save()
    return redirect('carrinho')


def carrinho(request):
    itens = CarrinhoItem.objects.filter(user=request.user)
    return render(request, 'vendas/carrinho.html', {'itens': itens})


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
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(username=username, email=email, password=password)
        return redirect('/login/')
    return render(request, 'vendas/cadastro.html')
