from django.db import migrations, models


def sincronizar_servicos_existentes(apps, schema_editor):
    ServicoAgenda = apps.get_model("agenda", "Servico")
    ServicoPainel = apps.get_model("servicos", "Servico")

    for painel in ServicoPainel.objects.all().iterator():
        ServicoAgenda.objects.update_or_create(
            nome=(painel.nome or "").strip(),
            defaults={
                "preco": painel.preco_padrao,
                "duracao_minutos": painel.duracao_min,
                "ativo": painel.ativo,
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("agenda", "0003_alter_agendamento_cliente"),
        ("servicos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="servico",
            name="ativo",
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(
            sincronizar_servicos_existentes,
            migrations.RunPython.noop,
        ),
    ]
