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