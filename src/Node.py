class Node:
    def __init__(self, id:int, pos = ()):
        self._id = id
        self._pos = pos
        self._weight = 0
        self._info = ""
        self._tag = 0

    def getID(self):
        return self._id

    def getPos(self):
        return self._pos

    def setPos(self, pos):
        self._pos = pos

    def getWeight(self):
        return self._weight

    def setWeight(self, weight):
        self._weight = weight

    def getInfo(self):
        return self._info

    def setInfo(self, info):
        self._info = info

    def getTag(self):
        return self._tag

    def setTag(self, tag):
        self._tag = tag

    def __repr__(self):
        return f"Node -> ID={self._id}"