import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodi = []
        self.getOrdinati = {}
        self.idMap = {}
        self._solBest = {}
        self._costBest = {}

    def buildGraph(self, calorie):
        self.idMap = dict()
        self._grafo.clear()
        self._nodi = DAO.getAllNodi(calorie)
        self._grafo.add_nodes_from(self._nodi)
        self.addEdgesPesati(calorie)
        for f in self._nodi:
            self.idMap[f.condiment_code] = f


    def addEdgesPesati(self, calorie):
        self._grafo.clear_edges()
        for n1 in self._grafo.nodes:
            for n2 in self._grafo.nodes:
                if n1.condiment_code != n2.condiment_code:
                    if self._grafo.has_edge(n1, n2) is False:
                        peso = DAO.getAllArchi(n1.condiment_code, n2.condiment_code)
                        if peso > 0:
                            self._grafo.add_edge(n1, n2, weight=peso)

    def getBestPath(self, v0):
        self._solBest = []
        self._costBest = 0
        parziale = []
        for v in self._grafo.nodes:
            parziale.append(v)
            self.ricorsione(parziale, v0)
            parziale.pop()
        return self._solBest, self._costBest

    def ricorsione(self, parziale, v0):
        if v0 in parziale:
            if self.peso(parziale) > self._costBest:
                self._costBest = self.peso(parziale)
                self._solBest = copy.deepcopy(parziale)

        for v in self._grafo.nodes:
            if v not in self._grafo.neighbors(parziale[-1]):
                if v not in parziale:
                    parziale.append(v)
                    self.ricorsione(parziale, v0)
                    parziale.pop()

    def peso(self, parziale):
        peso = 0
        for nodi in parziale:
            peso += nodi.condiment_calories
        return peso

    def stampaOrdinata(self):
        self.getOrdinati = {}
        for n1 in self._grafo.nodes:
            self.getOrdinati[n1.condiment_code] = 0
            for vicini in self._grafo.neighbors(n1):
                self.getOrdinati[n1.condiment_code] += self._grafo[n1][vicini]['weight']
        return self.getOrdinati

    def getCaratteristiche(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

