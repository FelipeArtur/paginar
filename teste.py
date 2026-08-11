"""Checagem do único trecho que já quebrou calado: a leitura do título.

    python teste.py
"""
import importlib.machinery
import importlib.util
import json
import pathlib
import tempfile

carregador = importlib.machinery.SourceFileLoader('paginar', str(pathlib.Path(__file__).parent / 'paginar'))
spec = importlib.util.spec_from_loader('paginar', carregador)
paginar = importlib.util.module_from_spec(spec)
carregador.exec_module(paginar)


def notebook(source):
    arquivo = pathlib.Path(tempfile.mkdtemp()) / 'meu-caderno.ipynb'
    arquivo.write_text(json.dumps({'cells': [{'cell_type': 'markdown', 'source': source}]}))
    return arquivo


# source como lista de linhas e como string única: nbformat aceita as duas.
assert paginar.titulo_do_notebook(notebook(['# Vendas 2025\n', 'texto'])) == 'Vendas 2025'
assert paginar.titulo_do_notebook(notebook('# Vendas 2025\ntexto')) == 'Vendas 2025'
# Sem título de nível 1, o nome do arquivo entra no lugar.
assert paginar.titulo_do_notebook(notebook('## Subtítulo')) == 'meu caderno'
print('ok')
