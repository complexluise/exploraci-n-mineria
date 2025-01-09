Explicación del Código: Análisis de Redes en la Minería Visible

Este artículo detalla el uso de la ciencia de redes para analizar los datos de minería visible en Colombia, utilizando Python y las bibliotecas pandas, networkx y matplotlib. A continuación, se explica el código paso a paso, cubriendo desde la carga de datos hasta la creación y visualización de gráficos de redes complejas.

1. Carga de Datos

import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)
Esta función, load_data, se encarga de cargar los datos desde un archivo CSV en un DataFrame de pandas. El DataFrame es una estructura tabular que facilita la manipulación y análisis de los datos, permitiendo realizar operaciones como filtrado, agregación y conversión.
2. Creación de la Red Bipartita
import networkx as nx

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
    return Bpy
Aquí se crea una red bipartita utilizando la biblioteca networkx. Una red bipartita es un tipo de red en la que los nodos pueden dividirse en dos conjuntos disjuntos, y las conexiones solo ocurren entre nodos de diferentes conjuntos. En este caso, los dos conjuntos son municipios y recursos naturales.
Nodos del tipo Municipio: Representan los municipios y almacenan información adicional como el valor de las regalías (regalias) y la cantidad de toneladas producidas (toneladas).
Nodos del tipo Recurso Natural: Representan los distintos recursos naturales explotados.
Aristas (Edges): Representan la relación de explotación entre un municipio y un recurso natural.

3. Identificación de los Principales Municipios
def get_top_municipalities(B, attribute, n=10):
    municipios = {n for n, d in B.nodes(data=True) if d['bipartite'] == 0}
    return sorted(municipios, key=lambda x: B.nodes[x][attribute], reverse=True)[:n]
Esta función extrae los municipios que tienen los mayores valores en un atributo específico (regalias o toneladas). Esto se utiliza para identificar los municipios más destacados en términos de producción o ingresos por regalías.
Ordenación: Los municipios se ordenan en orden descendente según el valor del atributo seleccionado.
Selección: Se seleccionan los n municipios con los valores más altos.

4. Visualización de los Principales Municipios
import matplotlib.pyplot as plt

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
Esta función genera gráficos de barras horizontales que visualizan los 10 principales municipios en términos de regalías y producción en toneladas. Se utilizan dos subgráficos, uno para cada métrica.
Gráfico de Regalías: Muestra los municipios ordenados por el valor de las regalías recibidas.
Gráfico de Toneladas Producidas: Muestra los municipios ordenados por la cantidad de toneladas de recursos naturales explotados.

5. Visualización de la Red Bipartita
def plpyot_bipartite_graph(B):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(B, k=0.1, iterations=20)
    nx.draw(B, pos, with_labels=True, 
            node_color=['#1f78b4' if B.nodes[node]['bipartite'] == 0 else '#33a02c' for node in B.nodes()],
            node_size=100, edge_color='gray', font_size=8)
    plt.title('Red Bipartita entre Municipios y Recursos Naturales')
    plt.show()
Aquí se dibuja la red bipartita utilizando un layout de resorte (spring_layout), que coloca los nodos de manera que minimiza la energía de la red, facilitando su interpretación visual.
Coloración de Nodos: Se utiliza un color diferente para municipios (azul) y recursos naturales (verde), ayudando a distinguir fácilmente los dos tipos de nodos.
Etiquetas y Tamaño de Nodos: Las etiquetas y tamaños de los nodos se ajustan para mejorar la legibilidad del gráfico.

6. Creación de la Red de Co-ocurrencia
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
Esta función genera una red de co-ocurrencia que conecta entidades que aparecen juntas en la misma agrupación. Por ejemplo, si dos recursos naturales son explotados en el mismo municipio, estarán conectados en la red.
Agrupación: Se agrupan los datos por un atributo (por ejemplo, municipio), y se genera una lista de las entidades asociadas (por ejemplo, recursos naturales).
Creación de Aristas: Se añade una arista entre cada par de entidades dentro de la misma agrupación, incrementando su peso si ya existe una conexión.

7. Guardado de Redes en Formato GraphML
def save_graph(G, file_path):
    nx.write_graphml(G, file_path)
Finalmente, esta función guarda la red generada en un archivo con formato GraphML, que es un formato estándar para la representación de grafos, ampliamente utilizado en aplicaciones de análisis de redes.
8. Ejecución del Script
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
    save_graph(B, 'datos/processed/red_bipartita_municipios_recursos.graphml')
    
    # Create and save co-occurrence graphs
    coocurrencia_recursos =  (df, 'municipio', 'recurso_natural')
    coocurrencia_municipios = create_cooccurrence_graph(df, 'recurso_natural', 'municipio')
    
    save_graph(coocurrencia_recursos, 'datos/processed/coocurrencia_recursos.graphml')
    save_graph(coocurrencia_municipios, 'datos/processed/coocurrencia_municipios.graphml')

if __name__ == "__main__":
    main()
Este bloque ejecuta todo el flujo de trabajo descrito, desde la carga de datos hasta la creación y visualización de gráficos de redes, y el guardado de estas redes en archivos para análisis posterior.