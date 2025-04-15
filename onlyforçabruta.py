import pygame
import random

# Configurações iniciais
largura_tela = 500
altura_tela = 500
cols, rows = 20, 20
w = largura_tela // cols

# Cores
COR_FUNDO = (30, 30, 30)
COR_PAREDE = (200, 200, 200)
COR_CAMINHO_FORCA_BRUTA = (255, 0, 0)

# Inicialização do PyGame
pygame.init()
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Labirinto - Força Bruta")
clock = pygame.time.Clock()

# Classe Celula
class Celula:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.paredes = [True, True, True, True]  # topo, direita, baixo, esquerda
        self.visitada = False

    def desenhar(self, tela, cor):
        x = self.i * w
        y = self.j * w

        if self.paredes[0]:
            pygame.draw.line(tela, COR_PAREDE, (x, y), (x + w, y), 2)
        if self.paredes[1]:
            pygame.draw.line(tela, COR_PAREDE, (x + w, y), (x + w, y + w), 2)
        if self.paredes[2]:
            pygame.draw.line(tela, COR_PAREDE, (x + w, y + w), (x, y + w), 2)
        if self.paredes[3]:
            pygame.draw.line(tela, COR_PAREDE, (x, y + w), (x, y), 2)

        if self.visitada:
            pygame.draw.rect(tela, cor, (x + 2, y + 2, w - 4, w - 4))

    def vizinhos_nao_visitados(self, grid):
        vizinhos = []
        direcoes = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for idx, (dx, dy) in enumerate(direcoes):
            ni, nj = self.i + dx, self.j + dy
            if 0 <= ni < cols and 0 <= nj < rows:
                vizinha = grid[nj][ni]
                if not vizinha.visitada:
                    vizinhos.append(vizinha)
        return vizinhos

def remover_paredes(a, b):
    dx = a.i - b.i
    dy = a.j - b.j
    if dx == 1:
        a.paredes[3] = False
        b.paredes[1] = False
    elif dx == -1:
        a.paredes[1] = False
        b.paredes[3] = False
    if dy == 1:
        a.paredes[0] = False
        b.paredes[2] = False
    elif dy == -1:
        a.paredes[2] = False
        b.paredes[0] = False

def gerar_labirinto():
    grid = [[Celula(i, j) for i in range(cols)] for j in range(rows)]
    atual = grid[0][0]
    atual.visitada = True
    visitados = 1

    while visitados < cols * rows:
        vizinhos = atual.vizinhos_nao_visitados(grid)
        if vizinhos:
            proxima = random.choice(vizinhos)
            remover_paredes(atual, proxima)
            atual = proxima
            atual.visitada = True
            visitados += 1
        else:
            nao_visitadas = [cell for linha in grid for cell in linha if cell.visitada]
            atual = random.choice(nao_visitadas)

    grid[1][0].paredes[3] = False  # Entrada
    grid[rows - 1][cols - 1].paredes[1] = False  # Saída

    return grid

# Função para resolver o labirinto usando Força Bruta (Backtracking)
def resolver_forca_bruta(grid):
    inicio = (0, 1)
    objetivo = (cols - 1, rows - 1)
    caminho = []

    def backtrack(i, j):
        if (i, j) == objetivo:
            caminho.append((i, j))
            return True
        celula = grid[j][i]
        direcoes = [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]
        for dx, dy, parede in direcoes:
            ni, nj = i + dx, j + dy
            if 0 <= ni < cols and 0 <= nj < rows and not celula.paredes[parede]:
                if (ni, nj) not in caminho:
                    caminho.append((ni, nj))
                    if backtrack(ni, nj):
                        return True
                    caminho.remove((ni, nj))
        return False

    backtrack(inicio[0], inicio[1])
    return caminho

def desenhar_caminho(caminho, cor):
    for i, j in caminho:
        x = i * w + 4
        y = j * w + 4
        pygame.draw.rect(tela, cor, (x, y, w - 8, w - 8))

def main():
    grid = gerar_labirinto()
    caminho_forca_bruta = resolver_forca_bruta(grid)

    rodando = True
    while rodando:
        tela.fill(COR_FUNDO)
        for linha in grid:
            for celula in linha:
                celula.desenhar(tela, (50, 50, 50))
        desenhar_caminho(caminho_forca_bruta, COR_CAMINHO_FORCA_BRUTA)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
