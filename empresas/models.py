from django.db import models


class Empresa(models.Model):
    """Empresa/Clínica (fundação Multi-clínica)."""

    nome = models.CharField(max_length=120)
    cnpj = models.CharField(max_length=18, blank=True, default="")
    telefone = models.CharField(max_length=30, blank=True, default="")
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome
