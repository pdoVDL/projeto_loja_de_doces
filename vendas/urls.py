from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('historico/', views.historico_vendas, name='historico_vendas'),
    path('cancelar/', views.cancelar_carrinho, name='cancelar_carrinho'),
    path('remover-unidade/<int:item_id>/', views.remover_uma_unidade, name='remover_uma_unidade'),
    path('remover-unidade/<int:item_id>/', views.remover_uma_unidade, name='remover_uma_unidade'),    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover-do-carrinho/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('finalizar/', views.finalizar_venda, name='finalizar_venda'),
]
