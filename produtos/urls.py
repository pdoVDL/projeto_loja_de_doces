from django.urls import path
from . import views

urlpatterns = [
    path('produtos/', views.produtos, name='produtos'),
    path('produtos/<int:produto_id>/', views.produto_detalhe, name='produto_detalhe'),

]