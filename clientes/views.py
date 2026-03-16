from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm

@login_required
def lista(request):
    q = request.GET.get("q", "").strip()
    qs = Cliente.objects.all().order_by("-id")
    if hasattr(Cliente, "empresa_id") and getattr(request, "empresa", None):
        qs = qs.filter(empresa=request.empresa)
    if q:
        qs = qs.filter(nome__icontains=q)
    return render(request, "clientes/lista.html", {"clientes": qs, "q": q})

@login_required
def novo(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            if hasattr(obj, "empresa_id") and getattr(request, "empresa", None) and not obj.empresa_id:
                obj.empresa = request.empresa
            obj.save()
            return redirect("clientes_lista")
    else:
        form = ClienteForm()
    return render(request, "clientes/form.html", {"form": form, "titulo": "Novo cliente"})

@login_required
def editar(request, pk):
    obj = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=obj)
        if form.is_valid():
            obj2 = form.save(commit=False)
            if hasattr(obj2, "empresa_id") and getattr(request, "empresa", None) and not obj2.empresa_id:
                obj2.empresa = request.empresa
            obj2.save()
            return redirect("clientes_lista")
    else:
        form = ClienteForm(instance=obj)
    return render(request, "clientes/form.html", {"form": form, "titulo": f"Editar cliente: {obj.nome}"})
