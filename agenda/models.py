from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

class Servico(models.Model):
    nome = models.CharField(max_length=150)
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    duracao_minutos = models.IntegerField(default=60)

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ("MARCADO", "Marcado"),
        ("CONFIRMADO", "Confirmado"),
        ("REALIZADO", "Realizado"),
        ("CANCELADO", "Cancelado"),
        ("FALTOU", "Faltou"),
    ]
    cliente = models.ForeignKey("clientes.Cliente", on_delete=models.CASCADE)
    profissional = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="MARCADO")
    observacoes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente} - {self.servico} ({self.inicio:%d/%m %H:%M})"

class Atendimento(models.Model):
    agendamento = models.OneToOneField(Agendamento, on_delete=models.CASCADE)
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Atendimento {self.agendamento}"

class AtendimentoProduto(models.Model):
    atendimento = models.ForeignKey(Atendimento, on_delete=models.CASCADE, related_name="produtos")
    produto = models.ForeignKey("loja.Produto", on_delete=models.PROTECT)
    quantidade = models.IntegerField(validators=[MinValueValidator(1)])
    custo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    custo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.custo_total = (self.custo_unitario or 0) * self.quantidade
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produto.nome} x{self.quantidade}"
