import json
import networkx as nx
import matplotlib.pyplot as plt

ruta_archivo = "OneDrive/Desktop/Malla interactiva python/Sistemas.json"

def leerJson(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
        return datos

def crear_grafo(datos):
    G = nx.DiGraph()

    # Agregar nodos con atributos
    for semestre, materias in datos["malla"].items():
        for materia, creditos in materias:
            G.add_node(materia, creditos=creditos, semestre=semestre)
    # Agregar aristas de prerrequisitos
    for materia, prereqs in datos["prerequisitos"].items():
        for prereq in prereqs:
            G.add_edge(prereq, materia)

    return G

# ============================
# FUNCIÓN: Calcular posiciones por semestre
# ============================
def posiciones_por_semestre(G):
    pos = {}
    semestres_raw = set(nx.get_node_attributes(G, 'semestre').values())

    # Diccionario para convertir romanos a números
    orden_romano = {
        "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
        "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10
    }

    # Ordenar correctamente según el número romano
    semestres = sorted(semestres_raw, key=lambda s: orden_romano.get(s, 999))

    x_gap = 5  # separación horizontal entre columnas
    y_gap = 2  # separación vertical entre nodos del mismo semestre

    for i, semestre in enumerate(semestres):
        nodos_semestre = [n for n, attr in G.nodes(data=True) if attr['semestre'] == semestre]
        nodos_semestre.sort()
        for j, nodo in enumerate(nodos_semestre):
            pos[nodo] = (i * x_gap, -j * y_gap)
    return pos

def dibujar_grafo(G):
    plt.figure(figsize=(20, 12))
    pos = posiciones_por_semestre(G)
    semestres_raw = set(nx.get_node_attributes(G, 'semestre').values())
    # Diccionario para convertir romanos a números
    orden_romano = {
        "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
        "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10
    }
    # Colores por semestre
    semestres = sorted(semestres_raw, key=lambda s: orden_romano.get(s, 999))
    import itertools
    colores_disponibles = itertools.cycle(plt.cm.tab10.colors)
    mapa_colores = {s: next(colores_disponibles) for s in semestres}
    colores = [mapa_colores[G.nodes[n]['semestre']] for n in G.nodes]

    # Dibujar nodos y aristas
    nx.draw(G, pos, with_labels=True, node_color=colores, node_size=2500,
            font_size=8, font_weight='bold', arrowsize=15, edge_color="gray")

    # Etiquetas de semestres en la parte superior
    for i, semestre in enumerate(semestres):
        plt.text(i * 5, 1, f"Semestre {semestre}", fontsize=12, ha='center', color='black', fontweight='bold')

    plt.title("Malla Curricular - Ingeniería de Sistemas")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# ============================
# FUNCIÓN PRINCIPAL
# ============================
def main():
    datos = leerJson(ruta_archivo)
    G = crear_grafo(datos)
    dibujar_grafo(G)

    # Ejemplos de uso
    print("\n📘 Ejemplos de consultas:\n")
    print("Prerrequisitos de Compiladores:", list(G.predecessors("Compiladores")))
    print("Materias que dependen de Calculo 1:", list(G.successors("Calculo 1")))
    print("¿Hay camino de Calculo 1 a Analisis de datos?:", nx.has_path(G, "Calculo 1", "Analisis de datos"))

    if nx.has_path(G, "Calculo 1", "Analisis de datos"):
        print("Ruta:", " → ".join(nx.shortest_path(G, "Calculo 1", "Analisis de datos")))

if __name__ == "__main__":
    main()
