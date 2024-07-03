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

    def creaGrafo(self, shape, state):
        self.grafo.clear()
        self.cities = DAO.getCity(state)
        self.grafo.add_nodes_from(self.cities)

        edgeW = DAO.getEdgeW(shape, state)
        for u, v, w in edgeW:
            self.grafo.add_edge(u, v, weight=w)

        stats = f"Nodi: {len(self.grafo.nodes)}, Spigoli: {len(self.grafo.edges)}"
        for c in self.grafo.nodes:
            tot = 0
            for v in self.grafo.neighbors(c):
                tot += self.grafo[c][v]['weight']
            stats += f"\n {c} peso={tot}"
        return stats

    def get_path(self, maxC):
        self.solBest = []
        self.maxPeso = 0

        for nodo in self.grafo.nodes:
            for vicino in self.grafo.neighbors(nodo):
                self.ricorsione([nodo, vicino], self.grafo[nodo][vicino]['weight'], maxC)

        return self.solBest, self.maxPeso

    def ricorsione(self, parziale, lastPeso, maxC):
        ultimo = parziale[-1]

        if len(parziale) > maxC:
            return
        if (self.getPeso(parziale) > self.maxPeso
                and len(parziale) == maxC):
            self.maxPeso = self.getPeso(parziale)
            self.solBest = copy.deepcopy(parziale)

        for vicino in self.grafo.neighbors(ultimo):
            peso = self.grafo[ultimo][vicino]['weight']
            if vicino not in parziale and peso < lastPeso:
                parziale.append(vicino)
                self.ricorsione(parziale, peso, maxC)
                parziale.pop()

    def getPeso(self, parziale):
        tot = 0
        for i in range(len(parziale) - 1):
            tot += self.grafo[parziale[i]][parziale[i + 1]]['weight']
        return tot
