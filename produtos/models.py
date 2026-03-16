from django.db import models
from loja.models import Produto as LojaProduto

class LegacyProduto(models.Model):
    """Tabela antiga criada no app produtos (produtos_produto).
    Mantida apenas para leitura/migração.
    """
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'produtos'
        managed = False
        db_table = "produtos_produto"
        verbose_name = "Produto (legacy)"
        verbose_name_plural = "Produtos (legacy)"

    def __str__(self):
        return self.nome

class Produto(LojaProduto):
    """Proxy para usar os produtos reais da Loja na tela de cadastro."""
    class Meta:
        proxy = True
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
