<p align="center">
  <img src="logo.png" alt="Ícone do paginar" width="112">
</p>

<h1 align="center">paginar</h1>

<p align="center">Convert HTML documents and Jupyter notebooks to PDF, one file or a batch.</p>

O `paginar` gera PDFs de currículos, relatórios e outros documentos HTML ou
notebooks Jupyter pelo terminal. Usa Chromium, sem precisar de LaTeX.

## Instalar

Requer Linux, Python 3.9 ou mais novo e `curl`.

```sh
mkdir -p ~/.local/bin
paginar_download=$(mktemp ~/.local/bin/.paginar.XXXXXX)
curl -fsSLo "$paginar_download" https://raw.githubusercontent.com/FelipeArtur/paginar/main/paginar &&
chmod +x "$paginar_download" &&
mv -f "$paginar_download" ~/.local/bin/paginar
```

Inclua `~/.local/bin` no `PATH` do seu shell. Para atualizar, repita os comandos.
O download substitui o executável depois de terminar, inclusive quando o caminho
instalado é um link para um clone local.

Na primeira conversão, o script instala as dependências em um ambiente Python
isolado e baixa o Chromium headless. Esse preparo exige internet. As próximas
execuções reutilizam o ambiente e o navegador baixado. O Python do sistema
continua com seus próprios pacotes.

## Converter documentos

```sh
paginar curriculo.html
paginar relatorio.ipynb
paginar documento.html outro.html analise.ipynb
paginar *.html
paginar notebooks/
```

Cada PDF fica ao lado da entrada, com o mesmo nome e extensão `.pdf`.
Uma pasta seleciona somente os notebooks `.ipynb` diretamente dentro dela.
Para HTML, informe os arquivos ou use um glob como `*.html`.

O lote compartilha um navegador. Notebooks também compartilham um conversor
nbconvert, carregado uma vez. Se um arquivo falhar, o comando informa o
problema e continua com os demais. O código de saída é `1` quando alguma entrada
ou conversão falha e `0` quando todas terminam. Entradas repetidas são processadas
uma vez; documentos que gerariam o mesmo PDF são sinalizados como conflito.

Uma nova conversão substitui o PDF existente depois que a impressão termina.
Se ela falhar, o PDF anterior permanece.

## HTML e notebooks

| Entrada | Tratamento |
| --- | --- |
| `.html` | Imprime o documento com seu CSS, tamanho de página e margens. |
| `.ipynb` | Converte as saídas salvas para HTML e aplica paginação A4. |

HTML mantém o layout do autor, com escala 1 e sem rodapé adicional. Você pode
usar `@page` no CSS para definir papel e margens. Isso serve, por exemplo, para
imprimir um currículo que já tem seu próprio template.

Notebooks usam A4 paisagem, escala 0,8 e rodapé com título e número da página.
O título vem do primeiro cabeçalho Markdown `#`, ou do nome do arquivo quando
o cabeçalho falta. O CSS tenta manter figuras e saídas na mesma página;
conteúdo maior que uma página ainda pode precisar de ajustes no documento.

```sh
paginar relatorio.ipynb --retrato
paginar relatorio.ipynb --sem-codigo
paginar --help
```

`--retrato` muda o papel do notebook para A4 retrato. `--sem-codigo` oculta as
células de código e mantém os resultados. As duas opções se aplicam a notebooks.

O `paginar` imprime as saídas salvas e não executa células. Para atualizá-las:

```sh
jupyter nbconvert --to notebook --execute --inplace relatorio.ipynb
```

## Dependências

HTML usa Playwright. Notebooks também usam nbconvert. Se o Python ativo já tem
os pacotes necessários, o script usa esse ambiente. Caso contrário, usa
`~/.cache/paginar/python<versão>/`. A variável `XDG_CACHE_HOME`, quando definida,
altera a raiz desse cache.

O Chromium usa o cache padrão do Playwright, normalmente
`~/.cache/ms-playwright`. Se os pacotes já estão instalados mas o navegador
falta, a mensagem de erro mostra o comando para baixá-lo.

Temporários de conversão são removidos ao terminar. O ambiente Python e o
navegador ficam disponíveis para outras execuções.

## Usar um clone local

O executável funciona direto do repositório:

```sh
git clone git@github.com:FelipeArtur/paginar.git
cd paginar
./paginar exemplo/documento-exemplo.html
./paginar exemplo/relatorio-exemplo.ipynb
```

O primeiro comando de conversão produz um PDF A4 em retrato. O segundo produz
um relatório A4 em paisagem com as saídas salvas do notebook.

## Exemplo e verificação

O [documento HTML](exemplo/documento-exemplo.html) tem texto e uma tabela, com
papel e margens definidos em CSS.

O [notebook de exemplo](exemplo/relatorio-exemplo.ipynb) contém dados sintéticos,
uma tabela e dois gráficos. Veja o [PDF](exemplo/relatorio-exemplo.pdf):

![Página de exemplo](exemplo/pagina-exemplo.png)

```sh
python tests/test_paginar.py
python tests/test_paginar.py --integracao
```

A primeira checagem usa somente a biblioteca padrão. A integração exige
Playwright, nbconvert e Chromium no ambiente de teste e verifica PDFs reais,
continuidade após falha e limpeza dos temporários.

## Licença

MIT.
