import pyomo.environ as pyo

coordenadas = {
    1: (20, 6),
    2: (22, 1),
    3: (9, 2),
    4: (3, 25),
    5: (21, 10),
    6: (29, 2),
    7: (14, 12)
}

modelo = pyo.ConcreteModel()


nodos = coordenadas.keys()


arcos = [(i, j) for i in nodos for j in nodos if i != j]


modelo.conexion = pyo.Var(arcos, within=pyo.Binary)

modelo.objetivo = pyo.Objective(
    expr=sum(coordenadas[i][0] * coordenadas[j][0] * modelo.conexion[i, j] for i, j in arcos),
    sense=pyo.minimize
)

modelo.restricciones = pyo.ConstraintList()
for nodo in nodos:
    modelo.restricciones.add(
        sum(modelo.conexion[i, nodo] for i in nodos if i != nodo) == 1
    )

for i, j in arcos:
    if i != j:
        distancia = ((coordenadas[i][0] - coordenadas[j][0])**2 + (coordenadas[i][1] - coordenadas[j][1])**2)**0.5
        modelo.restricciones.add(modelo.conexion[i, j] * distancia <= 20)

solver = pyo.SolverFactory('glpk')
result = solver.solve(modelo)

import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
for i, j in arcos:
    if modelo.conexion[i, j].value == 1:
        G.add_edge(i, j)

pos = {nodo: coordenadas[nodo] for nodo in nodos}
labels = {nodo: str(nodo) for nodo in nodos}

nx.draw(G, pos, with_labels=True, labels=labels, node_size=300)
plt.title("Red de Nodos")
plt.show()

print("Ruta de mínimo costo:")
for i, j in arcos:
    if modelo.conexion[i, j].value == 1:
        print(f"Nodo {i} -> Nodo {j}")
