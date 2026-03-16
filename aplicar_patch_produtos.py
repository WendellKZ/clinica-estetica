# Patch automático para corrigir:
# RuntimeError: Model class produtos.models.LegacyProduto doesn't declare an explicit app_label and isn't in INSTALLED_APPS.
#
# Uso (na raiz C:\Estetica):
#   python aplicar_patch_produtos.py
#
# O script:
# 1) Adiciona 'produtos' em INSTALLED_APPS (se não existir)
# 2) Garante produtos/apps.py e produtos/__init__.py
# 3) Adiciona Meta.app_label = 'produtos' na classe LegacyProduto (se ainda não existir)

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

def patch_settings():
    settings_path = ROOT / "estetica" / "settings.py"
    if not settings_path.exists():
        raise SystemExit(f"Não achei {settings_path}. Rode este script na raiz do projeto (onde está o manage.py).")

    txt = settings_path.read_text(encoding="utf-8")

    if re.search(r"['\"]produtos['\"]", txt):
        print("OK: 'produtos' já está em INSTALLED_APPS (ou aparece no settings).")
        return

    # Insere dentro do INSTALLED_APPS = [ ... ]
    m = re.search(r"INSTALLED_APPS\s*=\s*\[\s*", txt)
    if not m:
        raise SystemExit("Não encontrei o bloco INSTALLED_APPS = [ ... ] no settings.py")

    insert_at = m.end()
    insertion = "    'produtos',\n"
    txt2 = txt[:insert_at] + insertion + txt[insert_at:]

    settings_path.write_text(txt2, encoding="utf-8")
    print("OK: Adicionado 'produtos' em INSTALLED_APPS.")

def ensure_apps_py():
    pkg = ROOT / "produtos"
    pkg.mkdir(exist_ok=True)

    init_path = pkg / "__init__.py"
    if not init_path.exists():
        init_path.write_text("", encoding="utf-8")

    apps_path = pkg / "apps.py"
    if not apps_path.exists():
        apps_path.write_text(
            "from django.apps import AppConfig\n\n\n"
            "class ProdutosConfig(AppConfig):\n"
            "    default_auto_field = 'django.db.models.BigAutoField'\n"
            "    name = 'produtos'\n",
            encoding="utf-8",
        )
        print("OK: Criado produtos/apps.py")

def patch_models():
    models_path = ROOT / "produtos" / "models.py"
    if not models_path.exists():
        print("Aviso: Não achei produtos/models.py para ajustar app_label. Pulando.")
        return

    txt = models_path.read_text(encoding="utf-8")

    # Se já tem Meta app_label dentro de LegacyProduto, não mexe
    if re.search(r"class\s+LegacyProduto\s*\(.*?\):.*?class\s+Meta\s*:\s*.*?app_label\s*=\s*['\"]produtos['\"]", txt, flags=re.S):
        print("OK: LegacyProduto já tem Meta.app_label.")
        return

    # Localiza o início da classe LegacyProduto
    m = re.search(r"^(class\s+LegacyProduto\s*\(.*?\):\s*)$", txt, flags=re.M)
    if not m:
        print("Aviso: Não encontrei a classe LegacyProduto em produtos/models.py. Nada a fazer.")
        return

    # Encontra a primeira linha identada após o class para pegar o nível de indentação padrão (4 espaços)
    # Vamos inserir logo após a docstring/primeira linha de corpo se houver, mas com segurança: inserção depois da linha do class.
    lines = txt.splitlines(True)
    idx = None
    for i, line in enumerate(lines):
        if re.match(r"^class\s+LegacyProduto\s*\(.*?\):\s*$", line):
            idx = i
            break
    if idx is None:
        print("Aviso: Falha ao localizar a linha da classe LegacyProduto. Pulando.")
        return

    meta_block = (
        "    class Meta:\n"
        "        app_label = 'produtos'\n\n"
    )

    # Inserir após a linha 'class LegacyProduto...'
    lines.insert(idx+1, meta_block)
    models_path.write_text("".join(lines), encoding="utf-8")
    print("OK: Inserido Meta.app_label='produtos' em LegacyProduto.")

def main():
    ensure_apps_py()
    patch_settings()
    patch_models()
    print("\nPatch aplicado. Agora rode:")
    print("  python manage.py makemigrations produtos")
    print("  python manage.py migrate")
    print("  python manage.py runserver")

if __name__ == "__main__":
    main()
