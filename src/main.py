import pygame
import sys


TAMANHO_CELULA = 50 # Tamanho de cada quadradinho na tela em pixels
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
            pass # Por enquanto não faz nada, só vamos testar o visual
            
        # Pinta os quadradinhos na tela
        desenhar_grade(tela, grade_atual, linhas, colunas)
        
        # Atualiza a tela
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()