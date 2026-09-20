import pygame
import sys
import random
import copy
import os

# Configurações de Interface
LARGURA_DESEJADA = 800  # Largura total da janela
ALTURA_PAINEL = 130     # Altura do painel inferior

# Cores da Simulação (RGB)
COR_VAZIO = (200, 200, 200)       # 0: Solo Vazio
COR_ARVORE = (34, 139, 34)        # 1: Árvore
COR_FOGO = (255, 69, 0)           # 2: Fogo
COR_CINZAS = (105, 105, 105)      # 3: Cinzas
COR_FUNDO = (0, 0, 0)             # Borda das células
COR_PAINEL = (25, 25, 25)         # Fundo do painel
COR_TEXTO_DESTAQUE = (255, 215, 0) 

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

def gerar_mapa_aleatorio(linhas, colunas):
    """Gera uma matriz com distribuição probabilística inicial de floresta."""
    nova_matriz = []
    for _ in range(linhas):
        linha = []
        for _ in range(colunas):
            # Probabilidades: 70% Árvore, 25% Vazio, 5% Fogo inicial
            sorteio = random.random()
            if sorteio < 0.70:
                estado = 1  # Árvore[cite: 7]
            elif sorteio < 0.95:
                estado = 0  # Vazio[cite: 7]
            else:
                estado = 2  # Fogo[cite: 7]
            linha.append(estado)
        nova_matriz.append(linha)
    return nova_matriz

def desenhar_grade(tela, matriz, linhas, colunas, tamanho_celula):
    for x in range(linhas):
        for y in range(colunas):
            estado = matriz[x][y]
            
            if estado == 0: cor = COR_VAZIO
            elif estado == 1: cor = COR_ARVORE
            elif estado == 2: cor = COR_FOGO
            elif estado == 3: cor = COR_CINZAS
            
            pygame.draw.rect(
                tela, 
                cor, 
                (y * tamanho_celula, x * tamanho_celula, tamanho_celula - 1, tamanho_celula - 1)
            )

def desenhar_painel(tela, matriz, geracao, pausado, fonte_bold, fonte_sm, largura_tela, altura_grade):
    pygame.draw.rect(tela, COR_PAINEL, (0, altura_grade, largura_tela, ALTURA_PAINEL))
    
    # Contadores
    vazio = sum(linha.count(0) for linha in matriz)
    arvores = sum(linha.count(1) for linha in matriz)
    fogo = sum(linha.count(2) for linha in matriz)
    cinzas = sum(linha.count(3) for linha in matriz)
    
    status_txt = "PAUSADO" if pausado else "RODANDO"
    cor_status = (255, 100, 100) if pausado else (100, 255, 100)
    
    # Linha 1 - Info de Estado e População
    txt_geracao = fonte_bold.render(f"Geração: {geracao}", True, COR_TEXTO_DESTAQUE)
    txt_status = fonte_bold.render(f"Estado: {status_txt}", True, cor_status)
    txt_arvores = fonte_bold.render(f"Árvores: {arvores}", True, COR_ARVORE)
    txt_fogo = fonte_bold.render(f"Fogo: {fogo}", True, COR_FOGO)
    txt_cinzas = fonte_bold.render(f"Cinzas: {cinzas}", True, COR_CINZAS)
    txt_vazio = fonte_bold.render(f"Vazio: {vazio}", True, COR_VAZIO)
    
    tela.blit(txt_geracao, (15, altura_grade + 12))
    tela.blit(txt_status, (140, altura_grade + 12))
    tela.blit(txt_arvores, (290, altura_grade + 12))
    tela.blit(txt_fogo, (420, altura_grade + 12))
    tela.blit(txt_cinzas, (520, altura_grade + 12))
    tela.blit(txt_vazio, (630, altura_grade + 12))
    
    # Linha 2 - Informações das Regras
    txt_regras = fonte_sm.render(
        "Dinâmica: Raios/Combustão espontânea (0.2%) | Germinação contínua (1.5%)", 
        True, (170, 170, 170)
    )
    tela.blit(txt_regras, (15, altura_grade + 48))
    
    # Linha 3 - Comandos de Controle (Inclui Tecla G)
    txt_comandos = fonte_sm.render(
        "[ESPAÇO]: Play/Pause | [G]: Gerar Novo Mapa | [R]: Reset | [S]: Step | [Clique]: Alterar", 
        True, (220, 220, 220)
    )
    tela.blit(txt_comandos, (15, altura_grade + 78))

def contar_vizinhos_em_chamas(matriz, x, y, linhas, colunas):
    """Contagem usando Vizinhança de Moore (8 vizinhos)."""
    fogo_ao_redor = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            
            vizinho_x = x + i
            vizinho_y = y + j
            
            if 0 <= vizinho_x < linhas and 0 <= vizinho_y < colunas:
                if matriz[vizinho_x][vizinho_y] == 2:
                    fogo_ao_redor += 1
                    
    return fogo_ao_redor

def calcular_proxima_geracao(matriz_atual, linhas, colunas):
    proxima_matriz = copy.deepcopy(matriz_atual)
    
    P_RAIO = 0.002        # 0.2% de chance de combustão espontânea
    P_REGENERACAO = 0.015 # 1.5% de chance de nascer nova árvore[cite: 7]
    
    for x in range(linhas):
        for y in range(colunas):
            estado = matriz_atual[x][y]
            
            if estado == 2:
                proxima_matriz[x][y] = 3  # Fogo vira cinza[cite: 7]
            elif estado == 3:
                proxima_matriz[x][y] = 0  # Cinza vira solo vazio[cite: 7]
            elif estado == 1:
                fogo_perto = contar_vizinhos_em_chamas(matriz_atual, x, y, linhas, colunas)
                if fogo_perto >= 1:
                    proxima_matriz[x][y] = 2  # Inflamação por vizinhança[cite: 7]
                elif random.random() <= P_RAIO:
                    proxima_matriz[x][y] = 2  # Incêndio por raio
            elif estado == 0:
                if random.random() <= P_REGENERACAO:
                    proxima_matriz[x][y] = 1  # Regeneração florestal[cite: 7]
                    
    return proxima_matriz

def main():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(diretorio_atual, "estado_inicial.txt")

    linhas, colunas, grade_inicial = carregar_estado_inicial(caminho_arquivo)
    grade_atual = copy.deepcopy(grade_inicial)
    
    pygame.init()
    pygame.font.init()
    
    fonte_bold = pygame.font.SysFont("Arial", 15, bold=True)
    fonte_sm = pygame.font.SysFont("Arial", 13)
    
    tamanho_celula = LARGURA_DESEJADA // colunas
    largura_real = tamanho_celula * colunas
    altura_grade_real = tamanho_celula * linhas
    
    tela = pygame.display.set_mode((largura_real, altura_grade_real + ALTURA_PAINEL))
    pygame.display.set_caption("Simulador de Incêndio Florestal")
    
    relogio = pygame.time.Clock()
    
    rodando = True
    simulacao_pausada = True
    contador_geracao = 0
    
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    pos_x, pos_y = evento.pos
                    if pos_y < altura_grade_real:
                        coluna_clicada = pos_x // tamanho_celula
                        linha_clicada = pos_y // tamanho_celula
                        
                        if 0 <= linha_clicada < linhas and 0 <= coluna_clicada < colunas:
                            estado_atual = grade_atual[linha_clicada][coluna_clicada]
                            grade_atual[linha_clicada][coluna_clicada] = (estado_atual + 1) % 4
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    simulacao_pausada = not simulacao_pausada
                elif evento.key == pygame.K_g:
                    # Gera uma nova floresta completamente aleatória
                    grade_atual = gerar_mapa_aleatorio(linhas, colunas)
                    contador_geracao = 0
                elif evento.key == pygame.K_r:
                    # Reseta para o estado inicial lido do arquivo TXT
                    grade_atual = copy.deepcopy(grade_inicial)
                    simulacao_pausada = True
                    contador_geracao = 0
                elif evento.key == pygame.K_s or evento.key == pygame.K_RIGHT:
                    if simulacao_pausada:
                        grade_atual = calcular_proxima_geracao(grade_atual, linhas, colunas)
                        contador_geracao += 1
        
        if not simulacao_pausada:
            grade_atual = calcular_proxima_geracao(grade_atual, linhas, colunas)
            contador_geracao += 1
            
        tela.fill(COR_FUNDO)
        desenhar_grade(tela, grade_atual, linhas, colunas, tamanho_celula)
        desenhar_painel(tela, grade_atual, contador_geracao, simulacao_pausada, fonte_bold, fonte_sm, largura_real, altura_grade_real)
        
        pygame.display.flip()
        relogio.tick(5)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()