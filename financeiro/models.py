from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator

class LancamentoFinanceiro(models.Model):
    TIPO_CHOICES = [("ENTRADA", "Entrada"), ("SAIDA", "Saída")]
    ORIGEM_CHOICES = [
        ("PROCEDIMENTO", "Procedimento"),
        ("VENDA", "Venda"),
        ("OUTROS", "Outros"),
    ]

    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    origem = models.CharField(max_length=20, choices=ORIGEM_CHOICES, default="OUTROS")
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    descricao = models.CharField(max_length=255)

    categoria = models.CharField(max_length=100, blank=True)

    agendamento = models.ForeignKey("agenda.Agendamento", null=True, blank=True, on_delete=models.SET_NULL)
    venda = models.ForeignKey("loja.Venda", null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} R$ {self.valor} em {self.data}"
