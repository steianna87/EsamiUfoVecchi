import copy
import datetime

import networkx as nx

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

    def creaGrafo(self, day, year):
        self.grafo.clear()
        self.grafo.add_nodes_from(self.states)

        edge = DAO.getAllVicini(self.stateMap)
        sightings = DAO.getSightings(year, self.stateMap)
        sightMap = {s: {dato for st, dato in sightings if s == st} for s, dato in sightings}

        for u, v in edge:
            try:
                Sight1 = sightMap[u]
                Sight2 = sightMap[v]
                sightComuni = set()
                for id1, date1 in Sight1:
                    for id2, date2 in Sight2:
                        delta = (date1 - date2)
                        if id1 != id2 and (date1 - date2) <= datetime.timedelta(days=day):
                            sightComuni.add(id1)
                            sightComuni.add(id2)
                            print((u, v))
                self.grafo.add_edge(u, v, weight=len(sightComuni))
            except KeyError:
                self.grafo.add_edge(u, v, weight=0)

        '''edgeW = DAO.getAllPesiDeltDay(self.stateMap, day, year)
        for u, v, w in edgeW:
            self.grafo[u][v]['weight'] += w'''

        stats = (f"Nodi: {len(self.grafo.nodes)}, Spigoli: {len(self.grafo.edges)}\n"
                 f"Top5:")
        for n in self.grafo.nodes:
            tot = 0
            for v in self.grafo.neighbors(n):
                tot += self.grafo[n][v]['weight']
            stats += f"\n{n}, peso adiacenti={tot}"

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
