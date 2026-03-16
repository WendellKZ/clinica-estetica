from django import forms
from django.contrib.auth.models import User, Group

class UsuarioCreateForm(forms.ModelForm):
    password = forms.CharField(label="Senha", widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label="Confirmar senha", widget=forms.PasswordInput, min_length=8)
    groups = forms.ModelMultipleChoiceField(
        label="Perfis (grupos)",
        queryset=Group.objects.all().order_by("name"),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": "6"})
    )
    is_staff = forms.BooleanField(label="Pode acessar Admin do Django (staff)", required=False)
    is_superuser = forms.BooleanField(label="Admin total (superuser)", required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_active", "is_staff", "is_superuser", "groups"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    is_active = forms.BooleanField(label="Ativo", required=False, initial=True)

    def clean(self):
        data = super().clean()
        p1 = data.get("password")
        p2 = data.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "As senhas não conferem.")
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            self.save_m2m()
        return user


class UsuarioUpdateForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        label="Perfis (grupos)",
        queryset=Group.objects.all().order_by("name"),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": "6"})
    )
    is_staff = forms.BooleanField(label="Pode acessar Admin do Django (staff)", required=False)
    is_superuser = forms.BooleanField(label="Admin total (superuser)", required=False)
    is_active = forms.BooleanField(label="Ativo", required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_active", "is_staff", "is_superuser", "groups"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class ResetSenhaForm(forms.Form):
    password = forms.CharField(label="Nova senha", widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(label="Confirmar nova senha", widget=forms.PasswordInput, min_length=8)

    def clean(self):
        data = super().clean()
        p1 = data.get("password")
        p2 = data.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "As senhas não conferem.")
        return data
