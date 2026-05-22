import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# =========================
# CONEXIONES
# =========================

conexiones = {
    'Jiloyork':{'CDMX': 125, 'QRO':513},
    'MORELOS':{'QRO':524},
    'CDMX':{'Jiloyork': 125, 'QRO':423, 'HGO':491},
    'HGO':{'CDMX':491, 'QRO':356, 'MEXICALI':309, 'MTY':346},
    'QRO':{
        'SLP':203,
        'MORELOS':514,
        'Jiloyork':513,
        'CDMX':423,
        'MTY':603,
        'SONORA':437,
        'HGO':356,
        'MEXICALI':313,
        'AGS':599
    },
    'SLP':{'AGS':390, 'QRO':203},
    'AGS':{'SLP':390, 'QRO':599},
    'SONORA':{'QRO':437, 'MEXICALI':394},
    'MEXICALI':{'MTY':296, 'HGO':309, 'QRO':313},
    'MTY':{'MEXICALI':296, 'QRO':603, 'HGO':346}
}

# =========================
# STREAMLIT UI
# =========================

st.title("🚗 Búsqueda de Ruta - Uniform Cost Search")

ciudades = list(conexiones.keys())

origen = st.selectbox("Selecciona ciudad origen", ciudades)
destino = st.selectbox("Selecciona ciudad destino", ciudades)

# =========================
# ALGORITMO
# =========================

def costo_uniforme(grafo, inicio, fin):

    frontera = [(0, inicio, [inicio])]
    visitados = set()

    while frontera:

        frontera.sort(key=lambda x: x[0])

        costo, nodo, camino = frontera.pop(0)

        if nodo == fin:
            return camino, costo

        if nodo not in visitados:

            visitados.add(nodo)

            for vecino, peso in grafo[nodo].items():

                if vecino not in visitados:
                    nueva_ruta = camino + [vecino]
                    nuevo_costo = costo + peso

                    frontera.append(
                        (nuevo_costo, vecino, nueva_ruta)
                    )

    return None, None

# =========================
# BOTON
# =========================

if st.button("Buscar Ruta"):

    ruta, costo = costo_uniforme(
        conexiones,
        origen,
        destino
    )

    if ruta:

        st.success("Ruta encontrada")

        st.write("### Ruta")
        st.write(" ➜ ".join(ruta))

        st.write("### Costo Total")
        st.write(f"{costo} km")

        # =========================
        # GRAFO
        # =========================

        G = nx.Graph()

        for ciudad, vecinos in conexiones.items():

            for vecino, distancia in vecinos.items():

                G.add_edge(
                    ciudad,
                    vecino,
                    weight=distancia
                )

        plt.figure(figsize=(10,7))

        pos = nx.spring_layout(G, seed=42)

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color='lightblue',
            node_size=2500,
            font_size=10
        )

        labels = nx.get_edge_attributes(G, 'weight')

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=labels
        )

        # Resaltar ruta
        path_edges = list(zip(ruta, ruta[1:]))

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=path_edges,
            edge_color='red',
            width=4
        )

        st.pyplot(plt)

    else:
        st.error("No se encontró ruta")