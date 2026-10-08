"""Checagens sem dependências; use --integracao para gerar PDFs com Chromium.

    python tests/test_paginar.py
    python tests/test_paginar.py --integracao
"""
import importlib.machinery
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

script = pathlib.Path(__file__).resolve().parent.parent / 'paginar'
carregador = importlib.machinery.SourceFileLoader('paginar', str(script))
spec = importlib.util.spec_from_loader('paginar', carregador)
paginar = importlib.util.module_from_spec(spec)
carregador.exec_module(paginar)

with tempfile.TemporaryDirectory(prefix='paginar-testes-') as tmp:
    pasta = pathlib.Path(tmp)
    nb = pasta / 'meu-caderno.ipynb'
    for source, esperado in [(['# Vendas 2025\n', 'texto'], 'Vendas 2025'),
                             ('# Vendas 2025\ntexto', 'Vendas 2025'),
                             ('## Subtítulo', 'meu caderno')]:
        nb.write_text(json.dumps({'cells': [{'cell_type': 'markdown', 'source': source}]}))
        assert paginar.titulo_do_notebook(nb) == esperado

    doc = pasta / 'documento.HTML'
    doc.write_text('<!doctype html><meta charset="utf-8"><h1>Documento de teste</h1>')
    invalido = pasta / 'dados.txt'
    invalido.write_text('texto')
    alvos, erros = paginar.arquivos([str(doc), str(doc), str(nb),
                                    str(invalido), str(pasta / 'ausente.html')])
    assert alvos == [doc, nb] and len(erros) == 2
    nb.with_suffix('.html').write_text('mesmo destino')
    alvos, erros = paginar.arquivos([str(nb), str(nb.with_suffix('.html'))])
    assert alvos == [nb] and len(erros) == 1
    assert paginar.arquivos([str(pasta)])[0] == [nb]

    class PaginaComFalha:
        fechada = False

        def goto(self, *args, **kwargs):
            pass

        def pdf(self, path, **kwargs):
            pathlib.Path(path).write_bytes(b'PDF incompleto')
            raise OSError('falha de impressão simulada')

        def close(self):
            self.fechada = True

    class Navegador:
        def new_page(self):
            return pagina

    pagina = PaginaComFalha()
    pdf = doc.with_suffix('.pdf')
    pdf.write_bytes(b'PDF anterior')
    try:
        paginar.gerar(doc, 'landscape', False, Navegador())
        raise AssertionError('a falha de impressão deveria propagar')
    except OSError:
        pass
    assert pdf.read_bytes() == b'PDF anterior'
    assert pagina.fechada and not list(pasta.glob('.paginar-*'))

    if '--integracao' in sys.argv:
        exemplo = pasta / 'relatorio.ipynb'
        shutil.copyfile(script.parent / 'exemplo/relatorio-exemplo.ipynb', exemplo)
        quebrado = pasta / 'quebrado.ipynb'
        quebrado.write_text('{')
        quebrado.with_suffix('.pdf').write_bytes(b'PDF preservado')
        resultado = subprocess.run([sys.executable, str(script), str(quebrado),
                                     str(doc), str(exemplo), '--sem-codigo'],
                                    capture_output=True, text=True)
        assert resultado.returncode == 1, resultado.stderr
        assert 'falha ao converter' in resultado.stderr
        for entrada in (doc, exemplo):
            assert entrada.with_suffix('.pdf').read_bytes().startswith(b'%PDF-')
        assert quebrado.with_suffix('.pdf').read_bytes() == b'PDF preservado'
        assert not list(pasta.glob('.paginar-*'))
        print('integração: HTML e notebook gerados, falha isolada, temporários removidos')

print('ok')
