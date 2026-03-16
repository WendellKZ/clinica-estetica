from django.db import migrations

def forwards(apps, schema_editor):
    Legacy = apps.get_model("produtos", "Produto")  # estado antigo (tabela produtos_produto)
    LojaProduto = apps.get_model("loja", "Produto")

    # se a tabela legacy não existir (ou estiver vazia), não faz nada
    try:
        legacy_qs = Legacy.objects.all()
    except Exception:
        return

    for lp in legacy_qs:
        # evita duplicar: tenta achar por nome + preço_venda
        exists = LojaProduto.objects.filter(nome=lp.nome, preco_venda=lp.preco).exists()
        if not exists:
            LojaProduto.objects.create(
                nome=lp.nome,
                sku="",
                custo=getattr(lp, "custo", 0) or 0,
                preco_venda=lp.preco,
                estoque_atual=0,
                ativo=getattr(lp, "ativo", True),
            )

def backwards(apps, schema_editor):
    # Não removemos da loja em rollback (segurança)
    pass

class Migration(migrations.Migration):

    dependencies = [
        ("loja", "0001_initial"),
        ("produtos", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
