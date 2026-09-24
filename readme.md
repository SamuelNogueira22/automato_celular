# Simulador de Incêndio Florestal 🌲🔥

Este projeto implementa um autômato celular 2D para simular a propagação de incêndio em uma floresta e a regeneração natural da vegetação. A simulação é visualizada em uma grade representando diferentes estados celulares e pode ser controlada por teclado e mouse em tempo real.

## Objetivo

O objetivo do sistema é demonstrar como regras locais simples podem gerar comportamentos complexos em uma malha espacial. Nesse caso, a evolução da grade depende do estado das células vizinhas, criando padrões de queima, resfriamento e recolonização da área.

## Como o modelo funciona

A simulação usa uma grade bidimensional em que cada célula pode assumir um dos quatro estados abaixo:

| Valor | Estado | Cor | Descrição |
| :---: | --- | --- | --- |
| 0 | Vazio | Cinza claro | Solo sem vegetação |
| 1 | Árvore | Verde | Vegetação combustível |
| 2 | Fogo | Laranja/vermelho | Célula em combustão |
| 3 | Cinza | Cinza escuro | Área já queimada |

### Vizinhança

A regra de propagação utiliza a vizinhança de Moore com raio 1, ou seja, cada célula analisa os 8 vizinhos ao seu redor.

### Regras de transição

As regras implementadas no código são as seguintes:

1. Célula com estado 2 (fogo) vira 3 (cinza) na próxima geração.
2. Célula com estado 3 (cinza) vira 0 (vazio) na próxima geração.
3. Célula com estado 1 (árvore) vira 2 (fogo) se houver pelo menos 1 vizinho em chamas.
4. Célula com estado 1 (árvore) também pode pegar fogo por chance aleatória de raio, configurada em 0,2%.
5. Célula com estado 0 (vazio) pode regenerar uma árvore com probabilidade de 1,5%.

Essas transições são calculadas de forma síncrona, gerando uma nova matriz para a próxima geração.

## Funcionalidades

- Leitura do estado inicial a partir de um arquivo .txt
- Visualização gráfica da grade com Pygame
- Simulação em execução ou pausada
- Geração aleatória de novo mapa
- Reset para o cenário inicial
- Execução passo a passo
- Edição manual da grade com clique do mouse
- Painel com contagem por estado e informações do sistema

## Estrutura do projeto

```text
automato_celular/
├── readme.md
├── src/
│   ├── main.py
│   └── estado_inicial.txt
└── .gitignore
```

### Arquivos principais

- `src/main.py`: contém toda a lógica da simulação, interface gráfica e regras do autômato celular.
- `src/estado_inicial.txt`: define a grade inicial do ambiente, com as dimensões e os estados das células.

## Formato do arquivo de estado inicial

O arquivo de configuração segue o formato:

```text
linhas colunas
estado1 estado2 estado3 ...
...
```

Exemplo:

```text
5 5
1 1 1 0 0
1 2 1 0 1
1 1 1 1 1
0 0 1 1 1
0 1 1 0 0
```

A primeira linha informa a quantidade de linhas e colunas da matriz. As linhas seguintes contêm os valores de cada célula.

## Pré-requisitos

- Python 3
- Biblioteca Pygame

## Como executar

No terminal, na raiz do projeto:

```bash
python -m pip install pygame
python src/main.py
```

Se estiver usando o ambiente virtual do projeto, pode rodar também:

```bash
python src/main.py
```

## Controles

- Espaço: pausa/continua a simulação
- G: gera um novo mapa aleatório
- R: reinicia para o estado inicial carregado do arquivo
- S ou seta para a direita: executa uma etapa manualmente
- Clique com botão esquerdo: altera o estado da célula clicada

## Painel da interface

A interface mostra:

- geração atual
- estado da simulação (rodando/pausado)
- quantidade de árvores, fogo, cinzas e células vazias
- mensagem das regras ativas da simulação

## Observações técnicas

A aplicação usa:

- `pygame` para a rendering da interface
- `copy.deepcopy` para preservar matrizes entre gerações
- `random` para probabilidades de combustão e regeneração
- leitura direta de um arquivo `.txt` para carregar o cenário inicial

## Possíveis melhorias

Algumas evoluções interessantes para o projeto incluem:

- edição visual mais intuitiva por ferramenta de desenho
- botão de reinício em interface gráfica
- salvamento do cenário atual em arquivo
- ajuste de velocidade da simulação
- adição de vento, obstáculos ou regras ambientais mais realistas

## Conclusão

O projeto funciona como um exemplo prático de automato celular aplicado à dinâmica de ecossistemas, combinando computação científica, modelagem espacial e visualização interativa em tempo real.