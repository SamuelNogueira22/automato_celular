# Simulador de Incêndio Florestal 🌲🔥

Este projeto é um **Autômato Celular** desenvolvido para a disciplina de Computação Científica. Ele simula a propagação de um incêndio em uma floresta, bem como o processo de regeneração natural da vegetação.

## 📋 Visão Geral e Objetivo
O modelo equilibra simplicidade computacional e visualização gráfica intuitiva, demonstrando como regras locais em uma grade 2D geram padrões complexos de espalhamento de calor e renovação do ecossistema. O projeto cumpre todos os requisitos obrigatórios, incluindo a execução simultânea (buffer duplo), controles de Play/Pause e leitura de estado inicial via arquivo `.txt`.

## 📐 Topologia e Vizinhança
A simulação adota a **Vizinhança de Moore** ($r=1$), onde cada célula central interage com suas **8 células vizinhas**: norte, sul, leste, oeste e as quatro diagonais[cite: 6]. 
> **Por que Moore?** Essa vizinhança permite uma dispersão de chamas mais circular e orgânica (isotrópica) na grade bidimensional, evitando o padrão irreal em formato de cruz[cite: 6].

## 🎨 Representação dos Estados
Cada célula pertence a um conjunto finito de 4 estados possíveis[cite: 6]:

| Valor | Identificação | Representação Visual | Significado / Dinâmica |
| :---: | :--- | :--- | :--- |
| **0** | Vazio / Clareira | Cinza Claro | Solo sem vegetação. Sujeito a regeneração natural espontânea[cite: 6]. |
| **1** | Árvore / Floresta | Verde | Vegetação combustível saudável. Inflama quando em contato com calor vizinho[cite: 6]. |
| **2** | Fogo / Em Chamas | Laranja / Vermelho | Célula ativa em processo de queima. Propaga fagulhas para árvores adjacentes[cite: 6]. |
| **3** | Cinzas / Resíduo | Cinza Escuro | Material recém-queimado em resfriamento. Não propaga mais fogo[cite: 6]. |

## ⚙️ Regras de Transição (Dinâmica do Modelo)
A transição de tempo ocorre de maneira síncrona, aplicando as seguintes regras de evolução[cite: 6]:
1. **Evolução do Fogo:** Célula com estado `2` (Fogo) torna-se `3` (Cinzas) na iteração subsequente[cite: 6].
2. **Dissipação das Cinzas:** Célula com estado `3` (Cinzas) arrefece e torna-se `0` (Vazio)[cite: 6].
3. **Inflamação de Árvores:** Célula com estado `1` (Árvore) torna-se `2` (Fogo) se possuir **pelo menos 1 vizinho** em chamas[cite: 6].
4. **Regeneração Espontânea:** Célula com estado `0` (Vazio) possui probabilidade fixa de $0.5\%$ de germinar uma nova muda e transitar para o estado `1` (Árvore)[cite: 6].

## 🚀 Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o **Python** instalado na sua máquina, juntamente com a biblioteca **Pygame** para a interface gráfica.
```bash
pip install pygame

## 🔮 Expansões Futuras (Diferenciais em Desenvolvimento)

Para atender integralmente aos requisitos opcionais e diferenciais propostos na especificação do projeto[cite: 4], as seguintes funcionalidades estão mapeadas para o próximo ciclo de desenvolvimento:

*   **Controles de Passo e Reinício:** 
    *   Implementação da função *Step*, permitindo executar uma única iteração por vez para análise detalhada[cite: 4].
    *   Implementação da função *Reset*, para retornar a simulação ao seu estado inicial[cite: 4].
*   **Interação em Tempo Real:** Permitir que o usuário edite a grade com o mouse, incluindo desenhar ou apagar células diretamente na tela[cite: 4].
*   **Exportação de Cenários:** Adição de uma funcionalidade para salvar o estado atual do autômato em um novo arquivo de texto[cite: 4].
*   **Telemetria e Ajustes:** 
    *   Exibir informações em tempo real na interface, como o número de iterações e a quantidade de células em cada estado[cite: 4].
    *   Permitir que o usuário ajuste a velocidade da simulação dinamicamente[cite: 4].
*   **Elementos Criativos Avançados:** Adicionar variáveis ambientais e geográficas à regra de propagação, como a influência do vento ou a presença de obstáculos incombustíveis[cite: 4].