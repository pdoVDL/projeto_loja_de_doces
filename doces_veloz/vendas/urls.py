from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/<int:produto_id>/', views.produto_detalhe, name='produto_detalhe'),
    path('adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('finalizar/', views.finalizar_venda, name='finalizar_venda'),
    path('historico/', views.historico_vendas, name='historico_vendas'),
    path('cancelar/', views.cancelar_carrinho, name='cancelar_carrinho'),
    path('remover-unidade/<int:item_id>/', views.remover_uma_unidade, name='remover_uma_unidade'),
    path('remover-do-carrinho/<int:produto_id>/', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('accounts/login/', views.login_view),
    path('remover-unidade/<int:item_id>/', views.remover_uma_unidade, name='remover_uma_unidade'),
]
