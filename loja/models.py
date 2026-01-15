from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Produto(models.Model):
    nome = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, blank=True)
    custo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    estoque_atual = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Venda(models.Model):
    FORMA_CHOICES = [
        ("PIX", "Pix"),
        ("DINHEIRO", "Dinheiro"),
        ("CARTAO", "Cartão"),
    ]
    data = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey("clientes.Cliente", null=True, blank=True, on_delete=models.SET_NULL)
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_CHOICES, default="PIX")
    observacao = models.CharField(max_length=255, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venda #{self.id} - {self.data:%d/%m/%Y %H:%M}"

class VendaItem(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, null=True, blank=True)
    nome_produto = models.CharField(max_length=150, blank=True)
    quantidade = models.IntegerField(validators=[MinValueValidator(1)])
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    custo_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = (self.preco_unitario or 0) * self.quantidade
        self.custo_total = (self.custo_unitario or 0) * self.quantidade
        super().save(*args, **kwargs)

    def __str__(self):
        nome = self.produto.nome if self.produto else (self.nome_produto or "Item")
        return f"{nome} x{self.quantidade}"
