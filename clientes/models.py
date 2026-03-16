from django.db import models

class Cliente(models.Model):
    empresa = models.ForeignKey("empresas.Empresa", null=True, blank=True, on_delete=models.PROTECT, related_name="clientes")
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    observacoes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
