import networkx as nx
import matplotlib.pyplot as plt
import math


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


def inicializa_grafo(Grafo, numero_vertices, linhas):
    """Função utilizada para inicializar os vértices e as arestas do grafo."""
    
    for i in range(numero_vertices):
        Grafo.add_node(i)
    
    for i in range(numero_vertices):        
        linha = linhas[i].rstrip().split()
        u_x, u_y = int(linha[0]), int(linha[1])
        
        for j in range(numero_vertices):
            
            if i != j:
                linha = linhas[j].rstrip().split()
                v_x, v_y = int(linha[0]), int(linha[1])
                
                u = (u_x, u_y)
                v = (v_x, v_y)
                d = round(distancia_euclidiana(u, v))
                
                Grafo.add_edge(i, j, weight=d)
                
                
def desenha_grafo(Grafo):
    """Função utilizada para desenhar o grafo."""
    
    options = {
        "font_size": 10,
        "font_weight": "bold",
        "font_color": "#FFF8E8",
        "node_size": 240,
        "node_color": "#0B6E4F",
        "edge_color": "#011936"
    }
    
    pos = nx.spring_layout(Grafo)
    
    # Desenhando o grafo lido no arquivo de entrada:
    nx.draw(Grafo, **options, with_labels=True, pos=pos) 

    edge_labels = dict([((u,v,),d['weight'])

    for u, v, d in Grafo.edges(data=True)])
    nx.draw_networkx_edge_labels(Grafo, pos, edge_labels=edge_labels, font_size=options["font_size"])

    plt.savefig("grafo.png")  # Salvando o grafo desenhado como uma imagem "grafo.png".
    plt.show()
    
    
def tsp():
    
    linhas = ler_arquivo()

    if linhas:
    
        numero_vertices = int(linhas[0].rstrip())
        linhas.pop(0)
    
        Grafo = nx.Graph()
        
        inicializa_grafo(Grafo, numero_vertices, linhas)        
        desenha_grafo(Grafo)

    else:
        print("O arquivo de entrada não foi encontrado!")

tsp()