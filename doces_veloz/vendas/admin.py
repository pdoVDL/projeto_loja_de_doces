from django.contrib import admin
from .models import Produto, CarrinhoItem

# Register your models here.
admin.site.register(Produto)
admin.site.register(CarrinhoItem)