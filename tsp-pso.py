import math
import numpy as np
import random
import itertools


def ler_arquivo():
    """Função utilizada para ler as linhas do arquivo de entrada fornecido."""
    
    try:
        with open('instancia.txt') as obj_arquivo:
            linhas = obj_arquivo.readlines()
    
    except FileNotFoundError:
        return None
    
    else:
        return linhas
    
    
def distancia_euclidiana(u, v):
    """Calcula a distância euclidiana entre duas cidades."""
        
    return math.sqrt(pow(v[0] - u[0], 2) + pow(v[1] - u[1], 2))


def obter_coordenadas(coordenadas, linhas):
    """Obtêm as coordenadas de cada cidade."""
    
    numero_cidades = int(linhas[0].rstrip()) 
    linhas.pop(0)
    
    # Obtenha as coordenadas x e y de cada cidade:
    for linha in linhas:
        linha = linha.split()
        coordenadas.append((int(linha[0]), int(linha[1])))
    
    return coordenadas, numero_cidades


def inicializa_grafo(Grafo, numero_cidades, coordenadas):
    """
        Função utilizada para inicializar os vértices e as arestas do grafo.
        utilizando matriz de adjacência."""
        
    for i in range(numero_cidades):
        u = coordenadas[i]
        
        for j in range(numero_cidades):
            
            if i != j:
                v = coordenadas[j]
                d = round(distancia_euclidiana(u, v))
                
                Grafo[i][j] = d
                

def inicializar_particulas(N, numero_cidades):
    """Função utilizada para inicializar a população de partículas."""
    
    # Cada partícula é uma rota (possível solução)  para o TSP:
    
    particulas = []
    
    for _ in range(N):
        rota = list(np.random.permutation(numero_cidades))
        particulas.append(rota)
    
    return particulas
                  
                  
def inicializar_velocidades(numero_cidades):
    """"""

    # A velocidade será uma lista na qual, cada posição, terá uma lista de
    # tuplas de pares (i, j), onde i e j são os índices dos elementos
    # (cidades) da partícula que serão trocados:
    velocidade = []
    
    permutacoes = list(itertools.permutations(range(numero_cidades), 2))
    
    permutacoes_removidas = set()
    for (i, j) in permutacoes:
        if (j, i) not in permutacoes_removidas:
            permutacoes_removidas.add((i, j))
            
    permutacoes_removidas = list(permutacoes_removidas)
    
    for _ in range(numero_cidades):
        random.shuffle(permutacoes_removidas)
        velocidade.append(permutacoes_removidas)
        
    return velocidade
    
                  
def fitness(Grafo, rota, numero_cidades):
    """
        Projeta a função de adaptação (ou fitness) para avaliar cada indivíduo
        (cada solução). Calcula a distância total (custo) percorrida por uma
        partícula com base na distância entre cada cidade.
    """  
    
    distancia = 0
    for i in range(numero_cidades-1):
        distancia += Grafo[rota[i]][rota[i+1]]
    
    # Calcula a distância da última cidade para a cidade inicial:
    distancia += Grafo[rota[-1]][rota[0]]
    
    return distancia

def atualizar_velocidade(rota, nova_rota, velocidade):
    """
    Atualiza o vetor de velocidade de uma determinada partícula adicionando as
    tuplas de índices que deverão ser trocados.
    """
    
    copia_rota = rota[:] # representa uma cópia da rota atual da partícula.
    
    for i in range(len(copia_rota)):
        # Verificamos se a cidade está ou não na posição correta:
        if copia_rota[i] != nova_rota[i]:
            indice_troca = nova_rota.index(copia_rota[i])
            velocidade.append((i, indice_troca))
            
    return velocidade


def realizar_troca(rota, velocidade):
    """
    Atualiza o vetor de velocidade de uma determinada partícula adicionando as
    tuplas de índices que deverão ser trocados.
    """
    
    for (i, j) in velocidade:
        rota[i] = rota[j]
        rota[j] = rota[i]

        
def atualizar_particula(particula, N, velocidade, w, c1, c2, pBest, gBest):
    """"""
        
    pBest_diferenca = gBest_diferenca = []
    
    for i in range(N):
        pBest_diferenca.append(pBest[i] - particula[i])
        gBest_diferenca.append(gBest[i] - particula[i])
        
    pBest_diferenca = np.array(pBest_diferenca)
    gBest_diferenca = np.array(gBest_diferenca)
                
    for v in velocidade:
        
        r1 = random.random()
        r2 = random.random()
        
        v1 = (w * v[0]) + (c1 * r1 * pBest_diferenca) + (c2 * r2 * gBest_diferenca)
        v2 = (w * v[1]) + (c1 * r1 * pBest_diferenca) + (c2 * r2 * gBest_diferenca)

        v = (round(v1), round(v2))
    
    print("Velocidade atualizada:")
    print(velocidade)
    
    nova_particula = particula[:]
    realizar_troca(nova_particula, velocidade)
    for i in range(len(particula)):
        particula[i] = particula[i] + nova_particula[i]
                
                
def pso(N, M, w, c1, c2):
    """"""
    
    linhas = ler_arquivo()
              
    if linhas:
        coordenadas = []
        coordenadas, numero_cidades = obter_coordenadas(coordenadas, linhas)

        Grafo = [[0 for _ in range(numero_cidades)] for _ in range(numero_cidades)]
        inicializa_grafo(Grafo, numero_cidades, coordenadas)
        
        particulas = inicializar_particulas(N, numero_cidades)
        print("Partículas:")
        print(particulas)
            
        # pBesti (personal best): a melhor posição encontrada pela partícula i
        pBest = particulas[:]
        print("pbest: {}".format(pBest))
        
        pBest_custo = [fitness(Grafo, pBest[i], numero_cidades) for i in range(N)]        
        print("pbest_custo: " + str(pBest_custo))
        
        # gBest (global best): a melhor posição encontrada por todas as partículas
        gBest_custo = min(pBest_custo)
        print("gbest_custo: " + str(gBest_custo))
        gBest = pBest[pBest_custo.index(gBest_custo)]
        print("gbest: {}".format(gBest))
        
        velocidade = inicializar_velocidades(numero_cidades)
        
        for _ in range(M):
            for i in range(N):                
                custo_atual = fitness(Grafo, particulas[i], numero_cidades)
                
                if custo_atual < pBest_custo[i]:
                    pBest_custo[i] = custo_atual
                    pBest[i] = particulas[i]
                    
                if custo_atual < gBest_custo:
                    gBest_custo = custo_atual
                    gBest = particulas[i]
                
                print("Velocidade:")
                print(velocidade[i])
                    
                atualizar_particula(particulas[i], N, velocidade[i], w, c1, c2, pBest[i], gBest)
                    
        
        return gBest, gBest_custo
        
    else:
        print("O arquivo de entrada não foi encontrado!")


# N é o número de partículas no enxame
# M é o número de iterações
# c1 e c2 são parâmetros cognitivo e social (também chamados de taxas de 
# aprendizado)
# w é ponderação de inércia

gBest, gBest_custo = pso(N=10, M=100, c1=1.5, c2=1.5, w=0.7)

print("A melhor rota é: {}".format(gBest))
print("O custo da melhor rota é: {}".format(gBest_custo))