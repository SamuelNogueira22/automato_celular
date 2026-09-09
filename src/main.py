import pygame
import sys
import random
import copy


TAMANHO_CELULA = 140 # Tamanho de cada quadradinho na tela em pixels
LARGURA_TELA = 800
ALTURA_TELA = 600

# Cores baseadas na sua documentação (RGB)
COR_VAZIO = (200, 200, 200)   # 0: Cinza Claro
COR_ARVORE = (34, 139, 34)    # 1: Verde
COR_FOGO = (255, 69, 0)       # 2: Vermelho/Laranja
COR_CINZAS = (105, 105, 105)  # 3: Cinza Escuro
COR_FUNDO = (0, 0, 0)         # Preto para as linhas da grade

# Lê o arquivo de configuração para as matrizes
def carregar_estado_inicial(nome_arquivo):
    matriz = []
    with open(nome_arquivo, 'r') as arquivo:
        linhas_do_arquivo = arquivo.readlines()
        primeira_linha = linhas_do_arquivo[0].split()
        linhas_total = int(primeira_linha[0])
        colunas_total = int(primeira_linha[1])
        
        for i in range(1, linhas_total + 1):
            linha_atual = [int(numero) for numero in linhas_do_arquivo[i].split()]
            matriz.append(linha_atual)
            
    return linhas_total, colunas_total, matriz


def desenhar_grade(tela, matriz, linhas, colunas):
    tela.fill(COR_FUNDO) # Limpa a tela
    
    for x in range(linhas):
        for y in range(colunas):
            estado = matriz[x][y]
            
            # Descobre qual cor usar dependendo do número
            if estado == 0: cor = COR_VAZIO
            elif estado == 1: cor = COR_ARVORE
            elif estado == 2: cor = COR_FOGO
            elif estado == 3: cor = COR_CINZAS
            
            # Desenha o quadrado (tela, cor, (pos_X, pos_Y, largura, altura))
            # Multiplicar por TAMANHO_CELULA para não ficarem colados no canto
            pygame.draw.rect(tela, cor, (y * TAMANHO_CELULA, x * TAMANHO_CELULA, TAMANHO_CELULA - 1, TAMANHO_CELULA - 1))

def contar_vizinhos_em_chamas(matriz, x, y, linhas, colunas):
    fogo_ao_redor = 0
    # Percorre de -1 a 1 para x e y (os 8 vizinhos ao redor)
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue # Pula a própria célula central
            
            vizinho_x = x + i
            vizinho_y = y + j
            
            # Verifica se o vizinho está dentro dos limites da grade para não dar erro
            if 0 <= vizinho_x < linhas and 0 <= vizinho_y < colunas:
                if matriz[vizinho_x][vizinho_y] == 2: # 2 é o estado de Fogo
                    fogo_ao_redor += 1
                    
    return fogo_ao_redor

def calcular_proxima_geracao(matriz_atual, linhas, colunas):
    # Cria uma cópia da matriz para servir de buffer duplo
    proxima_matriz = copy.deepcopy(matriz_atual)
    
    for x in range(linhas):
        for y in range(colunas):
            estado = matriz_atual[x][y]
            
            # Regra 1: Fogo (2) vira Cinzas (3)
            if estado == 2:
                proxima_matriz[x][y] = 3
                
            # Regra 2: Cinzas (3) vira Vazio (0)
            elif estado == 3:
                proxima_matriz[x][y] = 0
                
            # Regra 3: Árvore (1) pega fogo se tiver >= 1 vizinho em chamas
            elif estado == 1:
                fogo_perto = contar_vizinhos_em_chamas(matriz_atual, x, y, linhas, colunas)
                if fogo_perto >= 1:
                    proxima_matriz[x][y] = 2
                    
            # Regra 4: Vazio (0) tem probabilidade de ~0.5% de virar Árvore (1)
            elif estado == 0:
                # random.random() gera um número entre 0.0 e 1.0 (0.005 = 0.5%)
                if random.random() <= 0.005:
                    proxima_matriz[x][y] = 1
                    
    return proxima_matriz


def main():
    # Carrega o mapa inicial
    linhas, colunas, grade_atual = carregar_estado_inicial("estado_inicial.txt")
    
    pygame.init()
    tela = pygame.display.set_mode((colunas * TAMANHO_CELULA, linhas * TAMANHO_CELULA))
    pygame.display.set_caption("Simulador de Incêndio Florestal")
    
    # Variáveis de controle
    rodando = True
    simulacao_pausada = True # Começa pausado para ver o estado inicial
    
    
    while rodando:
        # Verifica se o usuário apertou algum botão
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: # Clicou no X para fechar
                rodando = False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE: # Apertou Espaço
                    simulacao_pausada = not simulacao_pausada # Inverte entre Play e Pause
        
        
        if not simulacao_pausada:
            grade_atual = calcular_proxima_geracao(grade_atual, linhas, colunas)
            pygame.time.delay(300) # Pausa de 300 milissegundos para podermos ver a animação
            
        # Pinta os quadradinhos na tela
        desenhar_grade(tela, grade_atual, linhas, colunas)
        
        # Atualiza a tela
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()