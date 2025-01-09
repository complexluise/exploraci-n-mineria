import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def load_data(file_path):
    return pd.read_csv(file_path)

def create_bipartite_graph(df):
    B = nx.Graph()
    for _, row in df.iterrows():
        municipio = row['municipio']
        recurso = row['recurso_natural']
        regalias = row['valor_contraprestacion']
        toneladas = row['cantidad_produccion']
        
        B.add_node(municipio, bipartite=0, tipo='municipio', regalias=regalias, toneladas=toneladas)
        B.add_node(recurso, bipartite=1, tipo='recurso')
        B.add_edge(municipio, recurso)
    return B

def get_top_municipalities(B, attribute, n=10):
    municipios = {n for n, d in B.nodes(data=True) if d['bipartite'] == 0}
    return sorted(municipios, key=lambda x: B.nodes[x][attribute], reverse=True)[:n]

def plot_top_municipalities(B, top_municipios_regalias, top_municipios_toneladas):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    regalias_values = [B.nodes[municipio]['regalias'] for municipio in top_municipios_regalias]
    axes[0].barh(top_municipios_regalias, regalias_values, color='skyblue')
    axes[0].set_title('Top 10 Municipios por Regalías')
    axes[0].set_xlabel('Regalías')

    toneladas_values = [B.nodes[municipio]['toneladas'] for municipio in top_municipios_toneladas]
    axes[1].barh(top_municipios_toneladas, toneladas_values, color='lightgreen')
    axes[1].set_title('Top 10 Municipios por Toneladas Producidas')
    axes[1].set_xlabel('Toneladas')

    plt.tight_layout()
    plt.show()

def plot_bipartite_graph(B):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(B, k=0.1, iterations=20)
    nx.draw(B, pos, with_labels=True, 
            node_color=['#1f78b4' if B.nodes[node]['bipartite'] == 0 else '#33a02c' for node in B.nodes()],
            node_size=100, edge_color='gray', font_size=8)
    plt.title('Red Bipartita entre Municipios y Recursos Naturales')
    plt.show()

def create_cooccurrence_graph(df, group_by, other_entity):
    cooccurrence = nx.Graph()
    groups = defaultdict(list)
    
    for _, row in df.iterrows():
        groups[row[group_by]].append(row[other_entity])
    
    for entities in groups.values():
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                entity1, entity2 = entities[i], entities[j]
                if cooccurrence.has_edge(entity1, entity2):
                    cooccurrence[entity1][entity2]['weight'] += 1
                else:
                    cooccurrence.add_edge(entity1, entity2, weight=1)
    
    return cooccurrence

def save_graph(G, file_path):
    nx.write_graphml(G, file_path)

def main():
    # Load data
    df = load_data("datos/raw/Volúmen de explotación de minerales en Colombia.csv")
    
    # Create and analyze bipartite graph
    B = create_bipartite_graph(df)
    top_municipios_regalias = get_top_municipalities(B, 'regalias')
    top_municipios_toneladas = get_top_municipalities(B, 'toneladas')
    
    # Visualize results
    plot_top_municipalities(B, top_municipios_regalias, top_municipios_toneladas)
    plot_bipartite_graph(B)
    
    # Save bipartite graph
    save_graph(B, 'datos\processed\\red_bipartita_municipios_recursos.graphml')
    
    # Create and save co-occurrence graphs
    coocurrencia_recursos = create_cooccurrence_graph(df, 'municipio', 'recurso_natural')
    coocurrencia_municipios = create_cooccurrence_graph(df, 'recurso_natural', 'municipio')
    
    save_graph(coocurrencia_recursos, 'datos\processed\coocurrencia_recursos.graphml')
    save_graph(coocurrencia_municipios, 'datos\processed\coocurrencia_municipios.graphml')

if __name__ == "__main__":
    main()