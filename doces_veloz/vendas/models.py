# models.py
from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    imagem = models.ImageField(upload_to='produtos/')
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome

class CarrinhoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantidade * self.produto.preco

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} para {self.user.username}"
