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
                  
                  
def inicializar_velocidades(N, numero_cidades):
    """
    Função utilizada para inicializar a lista de velocidades na qual, cada 
    posição, terá uma lista de tuplas de pares (i, j), onde i e j são os 
    índices dos elementos (cidades) da partícula que serão trocados:
    """

    velocidade = []
    
    permutacoes = list(itertools.permutations(range(numero_cidades), 2))
    
    permutacoes_removidas = set()
    for (i, j) in permutacoes:
        if (j, i) not in permutacoes_removidas:
            permutacoes_removidas.add((i, j))
            
    permutacoes_removidas = list(permutacoes_removidas)
    
    for _ in range(N):
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

        
def atualizar_particula(particula, numero_cidades, velocidade, w, c1, c2, pBest, gBest):
    """
    Função utilizada para atualizar uma determinada partícula, realizando
    trocas nos índices das cidades e atualizando a posição da partícula.
    """
    
    solucao_particula = particula[:]
    solucao_pBest = pBest[:]
    solucao_gBest = gBest[:]
    temp_velocidade = []
    
    # inércia (manter parte da velocidade atual):
    temp_velocidade = [(i, j) for (i, j) in velocidade if random.random() < w]

    # Componente cognitiva (relação do pbest):
    for i in range(numero_cidades):
        if solucao_particula[i] != solucao_pBest[i] and random.random() < c1:
            operador_troca = (i, solucao_pBest.index(solucao_particula[i]))
            temp_velocidade.append(operador_troca)
            
            aux = solucao_pBest[operador_troca[0]]
            solucao_pBest[operador_troca[0]] = solucao_pBest[operador_troca[1]]
            solucao_pBest[operador_troca[1]] = aux

    # Componente social (relação do gbest):
    for i in range(numero_cidades):
        if solucao_particula[i] != solucao_gBest[i] and random.random() < c2:
            operador_troca = (i, solucao_gBest.index(solucao_particula[i]))
            temp_velocidade.append(operador_troca)
            
            aux = solucao_gBest[operador_troca[0]]
            solucao_gBest[operador_troca[0]] = solucao_gBest[operador_troca[1]]
            solucao_gBest[operador_troca[1]] = aux
        
    velocidade = temp_velocidade[:]
    
    for (i, j) in velocidade:
        aux = solucao_particula[i]
        solucao_particula[i] = solucao_particula[j]
        solucao_particula[j] = aux
        
    return solucao_particula
    
                            
def pso(N, M, w, c1, c2):
    """
    Algoritmo Particle Swarm Optmization (PSO) para solucionar o problema do
    caixeiro viajante (Travelling Salesman Problem - TSP):
    """
    
    linhas = ler_arquivo()
    
    if linhas:
        coordenadas = []
        coordenadas, numero_cidades = obter_coordenadas(coordenadas, linhas)

        Grafo = [[0 for _ in range(numero_cidades)] for _ in range(numero_cidades)]
        inicializa_grafo(Grafo, numero_cidades, coordenadas)
        
        particulas = inicializar_particulas(N, numero_cidades)
        print("Partículas:")
        for particula in particulas:
            print(particula)
        
        print()
            
        # pBesti (personal best): a melhor posição encontrada pela partícula i
        pBest = particulas[:]
        print("pbest inicial de cada partícula:")
        
        pBest_custo = [fitness(Grafo, pBest[i], numero_cidades) for i in range(N)]        
        for i in range(N):
            print("pbest: {}, Custo: {}".format(pBest[i], pBest_custo[i]))
        
        print()
        
        # gBest (global best): a melhor posição encontrada por todas as partículas
        gBest_custo = min(pBest_custo)
        gBest = pBest[pBest_custo.index(gBest_custo)]
        print("gbest inicial: {}, Custo: {}".format(gBest, gBest_custo))
        
        print()
        
        velocidade = inicializar_velocidades(N, numero_cidades)
                
        for _ in range(M):
            for i in range(N):                
                custo_atual = fitness(Grafo, particulas[i], numero_cidades)
                
                if custo_atual < pBest_custo[i]:
                    pBest_custo[i] = custo_atual
                    pBest[i] = particulas[i]
                    
                if custo_atual < gBest_custo:
                    gBest_custo = custo_atual
                    gBest = particulas[i]
                                
                particulas[i] = atualizar_particula(particulas[i], numero_cidades, velocidade[i], w, c1, c2, pBest[i], gBest)
        
        gBest.append(gBest[0])
        return gBest, gBest_custo
        
    else:
        print("O arquivo de entrada não foi encontrado!")


# Parâmetros utilizados no PSO:

# N é o número de partículas no enxame
# M é o número de iterações
# c1 e c2 são parâmetros cognitivo e social (também chamados de taxas de 
# aprendizado)
# w é ponderação de inércia

gBest, gBest_custo = pso(N=40, M=1000, w=0.7, c1=0.8, c2=0.9)

print()

print("A melhor rota é: {}".format(gBest))
print("O custo da melhor rota é: {}".format(gBest_custo))
