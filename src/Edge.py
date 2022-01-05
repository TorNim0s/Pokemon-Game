class Edge:

    def __init__(self, src:int, dst:int, weight:float):
        self._src = src
        self._dst = dst
        self._weight = weight
        self._info = ""
        self._tag = 0

    def getSrc(self):
        return self._src

    def getDst(self):
        return self._dst

    def getWeight(self):
        return self._weight

    def getInfo(self):
        return self._info

    def setTag(self,tag):
        self._tag = tag

    def getTag(self):
        return self._tag

    def __repr__(self):
        return f"Edge -> src({self._src}) -> dst({self._dst})"

