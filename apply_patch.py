import os
import re

TARGET_FILES = [
    os.path.join("templates", "agenda", "agenda.html"),
    os.path.join("templates", "base.html"),
    os.path.join("templates", "base_nav.html"),
]

REPLACEMENTS = [
    # {% url 'agenda' %} or {% url "agenda" %}
    (r"{%\s*url\s+['\"]agenda['\"]\s*%}", r"{% url 'agenda_lista' %}"),
    # {% url 'agenda' somearg %} -> agenda_lista (keep args)
    (r"{%\s*url\s+['\"]agenda['\"]\s+", r"{% url 'agenda_lista' "),
]

def patch_file(path: str) -> bool:
    if not os.path.exists(path):
        return False
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()

    dst = src
    for pattern, repl in REPLACEMENTS:
        dst = re.sub(pattern, repl, dst)

    if dst != src:
        with open(path, "w", encoding="utf-8") as f:
            f.write(dst)
        print(f"[OK] Ajustado: {path}")
    else:
        print(f"[SKIP] Nada para alterar: {path}")
    return True

def main():
    project_root = os.getcwd()
    found_any = False
    for rel in TARGET_FILES:
        abs_path = os.path.join(project_root, rel)
        if os.path.exists(abs_path):
            found_any = True
            patch_file(abs_path)

    if not found_any:
        print("[ERRO] Não encontrei templates/ na pasta atual. Rode este script na raiz do projeto (onde está o manage.py).")

    print("\nPronto. Agora rode:")
    print("  python manage.py runserver")
    print("\nSe ainda aparecer NoReverseMatch, procure em outros templates por:")
    print("  {% url 'agenda' %}")
    print("e troque por:")
    print("  {% url 'agenda_lista' %}")

if __name__ == "__main__":
    main()
