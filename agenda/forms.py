from datetime import timedelta
from django import forms

from .models import Agendamento
from clientes.models import Cliente

class AgendamentoForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all().order_by("nome"),
        required=False,
        empty_label="(Cadastrar na hora ou selecionar)",
    )
    cliente_nome = forms.CharField(required=False, label="Cliente (nome)")
    cliente_telefone = forms.CharField(required=False, label="Telefone")
    cliente_email = forms.EmailField(required=False, label="E-mail")

    duracao_min = forms.ChoiceField(
        required=False,
        label="Duração",
        choices=[
            ("30", "30 min"),
            ("45", "45 min"),
            ("60", "60 min"),
            ("90", "90 min"),
            ("120", "120 min"),
        ],
        initial="60",
    )

    class Meta:
        model = Agendamento
        fields = ["cliente", "profissional", "servico", "inicio", "fim", "status", "observacoes"]
        widgets = {
            "inicio": forms.DateTimeInput(attrs={"type":"datetime-local"}),
            "fim": forms.DateTimeInput(attrs={"type":"datetime-local"}),
            "observacoes": forms.Textarea(attrs={"rows":3}),
        }

    def clean(self):
        cleaned = super().clean()
        cliente = cleaned.get("cliente")
        nome = (cleaned.get("cliente_nome") or "").strip()

        if not cliente and not nome:
            raise forms.ValidationError("Selecione um cliente OU informe o nome do cliente para cadastrar na hora.")

        inicio = cleaned.get("inicio")
        fim = cleaned.get("fim")
        duracao = cleaned.get("duracao_min")

        if inicio and (not fim) and duracao:
            try:
                mins = int(duracao)
                cleaned["fim"] = inicio + timedelta(minutes=mins)
            except Exception:
                pass

        fim = cleaned.get("fim")
        if inicio and fim and fim <= inicio:
            raise forms.ValidationError("O horário de término deve ser maior que o horário de início.")

        return cleaned

    def get_or_create_cliente(self):
        cliente = self.cleaned_data.get("cliente")
        if cliente:
            return cliente
        nome = (self.cleaned_data.get("cliente_nome") or "").strip()
        tel = (self.cleaned_data.get("cliente_telefone") or "").strip()
        email = (self.cleaned_data.get("cliente_email") or "").strip()
        return Cliente.objects.create(nome=nome, telefone=tel, email=email)
