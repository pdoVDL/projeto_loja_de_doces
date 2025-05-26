from django.shortcuts import render, redirect,  get_object_or_404
from .models import Produto

# Create your views here.

def produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'produtos/produtos.html', {'produtos': produtos})


def produto_detalhe(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    return render(request, 'produtos/produto_detalhe.html', {'produto': produto})

