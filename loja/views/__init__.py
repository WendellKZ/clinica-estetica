# Exporta as views a partir de handlers.py (compat com loja/views/ como package)
from .handlers import *  # noqa

# Aliases para compatibilidade com urls antigos
def produtos_lista(request, *args, **kwargs):
    return produtos(request, *args, **kwargs)

def produtos_novo(request, *args, **kwargs):
    return produto_novo(request, *args, **kwargs)
