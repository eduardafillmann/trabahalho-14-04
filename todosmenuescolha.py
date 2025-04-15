import pygame
import random
import time
from collections import deque

# Configurações iniciais
largura_tela = 500
altura_tela = 500
cols, rows = 20, 20
w = largura_tela // cols

# Cores
COR_FUNDO = (30, 30, 30)
COR_PAREDE = (200, 200, 200)
COR_CAMINHO_BFS = (0, 0, 255)
COR_CAMINHO_DFS = (255, 0, 0)
COR_CAMINHO_A = (0, 255, 0)
COR_CAMINHO_FORCA_BRUTA = (255, 255, 0)

# Inicialização do PyGame
pygame.init()
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Labirinto - Algoritmos de Busca")
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

def desenhar_labirinto(grid):
    for linha in grid:
        for celula in linha:
            celula.desenhar(tela, (50, 50, 50))

# Funções de Algoritmos

# BFS
def resolver_bfs(grid):
    inicio = (0, 0)
    objetivo = (cols - 1, rows - 1)

    fila = deque([inicio])
    distancias = {inicio: 0}
    anterior = {inicio: None}
    visitados = set([inicio])

    while fila:
        atual = fila.popleft()
        i, j = atual

        if atual == objetivo:
            break

        direcoes = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in direcoes:
            ni, nj = i + dx, j + dy
            if 0 <= ni < cols and 0 <= nj < rows and (ni, nj) not in visitados:
                celula = grid[nj][ni]
                if not celula.paredes[dx + dy * 2]:
                    fila.append((ni, nj))
                    visitados.add((ni, nj))
                    distancias[(ni, nj)] = distancias[(i, j)] + 1
                    anterior[(ni, nj)] = (i, j)

    # Verifica se o objetivo foi alcançado antes de reconstruir o caminho
    caminho = []
    if objetivo in anterior:
        atual = objetivo
        while atual:
            caminho.append(atual)
            atual = anterior[atual]
        caminho = caminho[::-1]
    return caminho

# DFS
def resolver_dfs(grid):
    inicio = (0, 0)
    objetivo = (cols - 1, rows - 1)

    pilha = [inicio]
    distancias = {inicio: 0}
    anterior = {inicio: None}
    visitados = set([inicio])

    while pilha:
        atual = pilha.pop()
        i, j = atual

        if atual == objetivo:
            break

        direcoes = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in direcoes:
            ni, nj = i + dx, j + dy
            if 0 <= ni < cols and 0 <= nj < rows and (ni, nj) not in visitados:
                celula = grid[nj][ni]
                if not celula.paredes[dx + dy * 2]:
                    pilha.append((ni, nj))
                    visitados.add((ni, nj))
                    distancias[(ni, nj)] = distancias[(i, j)] + 1
                    anterior[(ni, nj)] = (i, j)

    # Reconstrução do caminho
    caminho = []
    if objetivo in anterior:
        atual = objetivo
        while atual:
            caminho.append(atual)
            atual = anterior[atual]
        caminho = caminho[::-1]
    return caminho

# Força Bruta
def resolver_forca_bruta(grid):
    caminho = []
    for i in range(cols):
        for j in range(rows):
            caminho.append((i, j))
    return caminho

# A*
def resolver_a_star(grid):
    inicio = (0, 0)
    objetivo = (cols - 1, rows - 1)

    open_list = [inicio]
    g = {inicio: 0}
    f = {inicio: g[inicio] + abs(inicio[0] - objetivo[0]) + abs(inicio[1] - objetivo[1])}
    anterior = {inicio: None}

    while open_list:
        atual = min(open_list, key=lambda x: f[x])
        if atual == objetivo:
            break

        open_list.remove(atual)
        i, j = atual
        direcoes = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in direcoes:
            ni, nj = i + dx, j + dy
            if 0 <= ni < cols and 0 <= nj < rows:
                celula = grid[nj][ni]
                if not celula.paredes[dx + dy * 2]:
                    novo_g = g[(i, j)] + 1
                    if (ni, nj) not in g or novo_g < g[(ni, nj)]:
                        g[(ni, nj)] = novo_g
                        f[(ni, nj)] = g[(ni, nj)] + abs(ni - objetivo[0]) + abs(nj - objetivo[1])
                        anterior[(ni, nj)] = (i, j)

    # Reconstrução do caminho
    caminho = []
    if objetivo in anterior:
        atual = objetivo
        while atual:
            caminho.append(atual)
            atual = anterior[atual]
        caminho = caminho[::-1]
    return caminho

# Função de Menu
def menu():
    print("Escolha o algoritmo de busca:")
    print("1 - BFS")
    print("2 - DFS")
    print("3 - Força Bruta")
    print("4 - A*")
    escolha = int(input("Digite o número do algoritmo: "))

    if escolha == 1:
        return resolver_bfs, COR_CAMINHO_BFS
    elif escolha == 2:
        return resolver_dfs, COR_CAMINHO_DFS
    elif escolha == 3:
        return resolver_forca_bruta, COR_CAMINHO_FORCA_BRUTA
    elif escolha == 4:
        return resolver_a_star, COR_CAMINHO_A
    else:
        print("Escolha inválida!")
        return menu()

# Função para executar o algoritmo
def executar_algoritmo(grid):
    resolver_funcao, cor = menu()
    caminho = resolver_funcao(grid)
    return caminho, cor

# Função principal
def main():
    grid = gerar_labirinto()
    caminho, cor = executar_algoritmo(grid)

    rodando = True
    while rodando:
        tela.fill(COR_FUNDO)
        desenhar_labirinto(grid)
        desenhar_caminho(caminho, cor)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
