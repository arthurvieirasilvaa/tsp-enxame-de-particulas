import networkx as nx

def ler_arquivo():
    """Função utilizada para ler o arquivo de entrada fornecido."""
    
    try:
        with open('instancia.txt') as obj_arquivo:
            conteudo = obj_arquivo.read()
    
    except FileNotFoundError:
        return None
    
    else:
        return conteudo
    
conteudo = ler_arquivo()

if conteudo:
    print(conteudo)

else:
    print("O arquivo de entrada não foi encontrado!")
    
edgelist = [(0, 1), (1, 2), (2, 3)]
H = nx.Graph(edgelist)  # create a graph from an edge list
list(H.edges())

print(H.nodes())