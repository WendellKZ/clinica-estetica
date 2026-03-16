from django.db import models

class Servico(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    duracao_min = models.PositiveIntegerField(default=60, help_text="Duração em minutos (para agenda).")
    preco_padrao = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custo_padrao = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Custo médio (para lucro real).")
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome
