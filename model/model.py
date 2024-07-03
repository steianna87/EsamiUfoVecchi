import copy

import networkx as nx
from geopy.distance import distance

from database.DAO import DAO


class Model:
    def __init__(self):
        self.cities = None
        self.maxPeso = None
        self.solBest = None
        self.selectedStates = None
        self.states = DAO.getAllStates()
        self.stateMap = {s.id: s for s in self.states}

        self.grafo = nx.Graph()

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllShapes(self):
        return DAO.getAllShape()

    def detStates(self):
        self.selectedStates = DAO.getStateSight()
        return [self.stateMap[stateId.upper()] for stateId in self.selectedStates]

    def creaGrafo(self, shape, year):
        self.grafo.clear()
        self.cities = DAO.getCity2(shape, year)
        self.grafo.add_nodes_from(self.cities)

        edgeW = DAO.getEdgeW2(shape, year)

        for u, v, w in edgeW:
            self.grafo.add_edge(u, v, weight=w)
            print(w)

        stats = (f"Nodi: {len(self.grafo.nodes)}, Spigoli: {len(self.grafo.edges)}\n"
                 f"Top5:")
        top5 = []
        for n in self.grafo.nodes:
            tot = 0
            for v in self.grafo.neighbors(n):
                tot += self.grafo[n][v]['weight']
            top5.append((n, tot))
        top5.sort(key=lambda x: x[1], reverse=True)
        for i in range(len(top5)):
            if i == 5:
                break
            stats += f"\n{top5[i][0]} peso={top5[i][1]}"
        return stats

    def get_path(self, target, maxD, minC):
        self.solBest = []
        self.maxPeso = 0

        for vicino in self.grafo.neighbors(target):
            self.ricorsione([target, vicino], self.grafo[target][vicino]['weight'], minC, maxD)

        return self.solBest, self.maxPeso

    def ricorsione(self, parziale, lastPeso, minC, maxD):
        ultimo = parziale[-1]
        if self.getPeso(parziale) > maxD:
            return

        if len(parziale) >= minC:
            if (self.getPeso(parziale) > self.maxPeso):
                self.maxPeso = self.getPeso(parziale)
                self.solBest = copy.deepcopy(parziale)

        for vicino in self.grafo.neighbors(ultimo):
            peso = self.grafo[ultimo][vicino]['weight']
            if vicino not in parziale and peso > lastPeso:
                parziale.append(vicino)
                self.ricorsione(parziale, peso, minC, maxD)
                parziale.pop()

    def getPeso(self, parziale):
        tot = 0
        for i in range(len(parziale) - 1):
            tot += self.grafo[parziale[i]][parziale[i + 1]]['weight']
        return tot
