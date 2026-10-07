<p align="center">
  <img src="logo.png" alt="Ícone do paginar" width="112">
</p>

<h1 align="center">paginar</h1>

<p align="center"><strong>Convert Jupyter notebooks and HTML files to paginated PDFs from the command line, without LaTeX.</strong></p>

Converta notebooks Jupyter e currículos HTML em PDF pelo terminal. O `paginar`
gera arquivos prontos para guardar ou compartilhar.

## Instalar

Requer Python 3.9 ou mais novo, `curl` e `~/.local/bin` no `PATH`.
O instalador baixa um único arquivo executável. Se o shell não encontrar
`paginar`, confira se `~/.local/bin` está no `PATH`.

```sh
mkdir -p ~/.local/bin
curl -fsSLo ~/.local/bin/paginar https://raw.githubusercontent.com/FelipeArtur/paginar/main/paginar
chmod +x ~/.local/bin/paginar
```

## Uso rápido

```sh
paginar curriculo.html
paginar relatorio.ipynb
paginar notebooks/
paginar *.ipynb
```

O PDF fica ao lado do arquivo de entrada, com o mesmo nome-base e extensão
`.pdf`. Uma pasta processa os arquivos `.ipynb` que estão nela; a busca não é
recursiva.

## Opções

| Comando | Efeito |
| --- | --- |
| `paginar arquivo.ipynb` | Gera um PDF em A4 paisagem. |
| `paginar arquivo.ipynb --retrato` | Gera o PDF em A4 retrato. |
| `paginar arquivo.ipynb --sem-codigo` | Oculta células de código e mantém resultados. |
| `paginar arquivo.html` | Imprime o HTML respeitando o layout do documento. |
| `paginar pasta/` | Processa notebooks `.ipynb` dentro da pasta. |
| `paginar --help` | Mostra todas as opções. |

As opções `--retrato` e `--sem-codigo` se aplicam a notebooks.

## Como cada arquivo é tratado

| Entrada | Resultado |
| --- | --- |
| Notebook `.ipynb` | Converte para HTML, incorpora imagens e aplica o layout de impressão. |
| Arquivo `.html` | Usa o layout definido no próprio documento; não injeta CSS nem rodapé. |
| Pasta | Processa apenas arquivos `.ipynb` diretamente dentro dela. HTML precisa ser informado pelo caminho. |

Notebooks saem em A4 paisagem, com escala 0,8 e rodapé. O título do rodapé vem
do primeiro cabeçalho Markdown `#`; sem esse cabeçalho, usa o nome do arquivo.
Figuras e saídas recebem regras para evitar quebras entre páginas.

HTML é tratado como documento pronto. Assim, um currículo que já define
`@page`, margens e escala mantém o layout que você preparou.

## Atualizar saídas do notebook

O `paginar` não executa o notebook. Ele imprime as saídas que já estão salvas
no arquivo. Se elas estiverem vazias ou desatualizadas, execute o notebook
antes:

```sh
jupyter nbconvert --to notebook --execute --inplace relatorio.ipynb
```

## Dependências e cache

Quando o Python atual já tem `nbconvert` e `playwright`, o `paginar` usa esse
ambiente. Caso contrário, cria um ambiente temporário e instala as dependências
a cada execução. Isso costuma acrescentar cerca de 15 segundos. Na primeira
execução, também baixa o Chromium headless; é preciso ter acesso à internet.
O ambiente temporário é removido ao fim de cada execução.

O Chromium headless fica em `~/.cache/ms-playwright` e pode ser compartilhado
com outras ferramentas Playwright. O cache usa cerca de 262 MB. O `paginar`
baixa apenas o `chromium-headless-shell`; o pacote Chromium completo usaria
mais 389 MB.

Para apagar o cache quando nenhuma outra ferramenta depender dele:

```sh
rm -rf ~/.cache/ms-playwright
```

## Exemplo

O notebook [`exemplo/relatorio-exemplo.ipynb`](exemplo/relatorio-exemplo.ipynb)
gera uma tabela e dois gráficos. O PDF resultante tem três páginas A4 paisagem:
[`exemplo/relatorio-exemplo.pdf`](exemplo/relatorio-exemplo.pdf).

![Página de exemplo](exemplo/pagina-exemplo.png)

## Licença

MIT.
