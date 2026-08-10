# nb2pdf

Converte notebook Jupyter em PDF paginado, direto do terminal, sem LaTeX e sem
passar pela impressão do Colab.

![Página de exemplo](exemplo/pagina-exemplo.png)

## Por que

Imprimir notebook pelo navegador quase sempre corta tabela larga na margem
direita, parte figura no meio da página e não numera folha. Exportar por LaTeX
resolve, mas exige uma instalação de TeX inteira só para isso.

O `nb2pdf` renderiza o notebook em HTML, injeta um CSS de impressão e manda o
Chromium do Playwright imprimir. A folha sai em A4 deitado, a tabela cabe, a
figura não se parte e o rodapé traz título e número da página.

## Instalação

```sh
mkdir -p ~/.local/bin
curl -fsSLo ~/.local/bin/nb2pdf https://raw.githubusercontent.com/FelipeArtur/nb2pdf/main/nb2pdf
chmod +x ~/.local/bin/nb2pdf
```

É um arquivo só. Na primeira execução ele monta o próprio ambiente em
`~/.local/share/nb2pdf` com `nbconvert`, `playwright` e o Chromium, o que leva
cerca de um minuto. Depois disso a conversão é instantânea e nada é instalado no
Python do sistema.

Requisitos: Python 3.9 ou mais novo e `~/.local/bin` no `PATH`.

## Uso

```sh
nb2pdf caderno.ipynb                 # PDF ao lado do notebook
nb2pdf pasta/                        # todos os .ipynb da pasta
nb2pdf *.ipynb --out ~/entregas      # destino próprio
nb2pdf caderno.ipynb --abrir         # abre o PDF ao terminar
nb2pdf caderno.ipynb --sem-codigo    # só texto e resultados
nb2pdf caderno.ipynb --retrato       # A4 em pé
nb2pdf caderno.ipynb --escala 0.7    # aperta mais, para tabela muito larga
```

## O que ele faz com o layout

- **A4 deitado com escala 0,8.** É o que faz caber uma tabela de dez ou mais
  colunas. Em retrato, `pandas` estoura a margem e o Chromium corta o resto.
- **Não parte figura nem tabela.** Cada saída sai inteira em uma folha só, e
  título não fica órfão no pé da página.
- **Rodapé com título e número da página.** O título vem do primeiro `#` do
  notebook, não do nome do arquivo.
- **Imagens embutidas.** O PDF não depende de arquivo externo nem de rede.

## O que ele não faz

Não executa o notebook. Ele imprime as saídas que já estão salvas no `.ipynb`,
que é o que você vê ao abrir o arquivo. Se as saídas estiverem vazias ou
desatualizadas, rode antes:

```sh
jupyter nbconvert --to notebook --execute --inplace caderno.ipynb
```

A execução fica de fora de propósito: ela precisaria das dependências do seu
notebook (`pandas`, `scipy`, o que for), e o ambiente do `nb2pdf` só carrega o
necessário para imprimir.

## Exemplo

`exemplo/relatorio-exemplo.ipynb` gera dados sintéticos, monta uma tabela de sete
colunas e dois gráficos. O PDF correspondente está em
`exemplo/relatorio-exemplo.pdf`, e a imagem do topo deste README é a segunda
página dele.

```sh
nb2pdf exemplo/relatorio-exemplo.ipynb --abrir
```

## Licença

MIT.
