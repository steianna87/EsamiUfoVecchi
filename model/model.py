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

        self.grafo = nx.DiGraph()

    def getAllYears(self):
        return DAO.getAllYears()

    def getYearsAndSight(self):
        return DAO.getYearAndSight()

    def getAllShapes(self):
        return DAO.getAllShape()

    def detStates(self):
        self.selectedStates = DAO.getStateSight()
        return [self.stateMap[stateId.upper()] for stateId in self.selectedStates]

    def creaGrafo(self, year):
        self.grafo.clear()
        self.selectedStates = DAO.getStatesBy(year, self.stateMap)
        self.grafo.add_nodes_from(self.selectedStates)

        DiEdges = DAO.getArchi(year, self.stateMap)
        self.grafo.add_edges_from(DiEdges)

        stats = f"Nodi: {len(self.grafo.nodes)}, Archi: {len(self.grafo.edges)}\n"
        return stats

    def getAnalisi(self, state):
        pred = list(self.grafo.predecessors(state))
        succ = list(self.grafo.successors(state))
        conn = list(nx.dfs_tree(self.grafo, state))
        return pred, succ, conn

    def get_path(self, state):
        self.solBest = []

        for succ in self.grafo.successors(state):
            self.ricorsione([state, succ])

        return self.solBest

    def ricorsione(self, parziale):
        ultimo = parziale[-1]

        if len(parziale) > len(self.solBest):
            self.solBest = copy.deepcopy(parziale)
            print(parziale)

        for succ in self.grafo.successors(ultimo):
            if succ not in parziale:
                parziale.append(succ)
                self.ricorsione(parziale)
                parziale.pop()

    def getPeso(self, parziale):
        tot = 0
        for i in range(len(parziale) - 1):
            tot += self.grafo[parziale[i]][parziale[i + 1]]['weight']
        return tot
