import sys
from pprint import pprint


class Block:
    def __init__(self, index, starts, size):
        self.index = index
        self.starts = starts
        self.size = size
        self.isFree = index is None

    @property
    def ends(self):
        return self.starts + self.size

    def __repr__(self):
        return f"[{self.index}] [{self.starts}:{self.ends}] s={self.size} isFree={self.isFree}"


class DiskMap:
    @staticmethod
    def parse(filename):
        with open(filename) as f:
            line = f.read()
        return [int(x) for x in line.strip()]

    def __init__(self, map):
        self.originalMap = map
        self.totalSize = sum(map)
        self.originalBlocks = self._getBlocks(map)
        self.layout = self._getLayoutFromBlocks()

    def _getBlocks(self, map):
        l = []
        runningBlockPosition = 0
        for i, size in enumerate(map):
            isFreeSpace = i % 2
            blockIndex = i // 2 if not isFreeSpace else None
            start = runningBlockPosition
            runningBlockPosition = runningBlockPosition + size
            b = Block(blockIndex, start, size)
            l.append(b)
        return l

    def _getLayoutFromBlocks(self):
        l = ["." for _ in range(self.totalSize)]
        activeBlocks = [b for b in self.originalBlocks if not b.isFree]
        for b in activeBlocks:
            for i in range(b.starts, b.ends):
                l[i] = str(b.index)
        return l

    def __repr__(self):
        return "".join(self.layout)

    def freeSpaceConsecutive(self):
        reorderedBlocks = self.originalBlocks[:]
        freeAscIter = (i for i, b in enumerate(reorderedBlocks) if b.isFree)
        leftmostFree = next(freeAscIter)
        lastMovableOccupied = len(reorderedBlocks) - 1
        while reorderedBlocks[lastMovableOccupied].isFree:
            lastMovableOccupied -= 1

        while lastMovableOccupied > 0:
            if leftmostFree > lastMovableOccupied:
                freeAscIter = (i for i, b in enumerate(reorderedBlocks) if b.isFree)
                leftmostFree = next(freeAscIter)
                if leftmostFree > lastMovableOccupied:
                    break
            print(
                "startloop",
                reorderedBlocks[leftmostFree],
                reorderedBlocks[lastMovableOccupied],
                sep="\n",
            )
            while (
                reorderedBlocks[leftmostFree].size
                < reorderedBlocks[lastMovableOccupied].size
            ):
                print(
                    "toobig",
                    reorderedBlocks[leftmostFree],
                    reorderedBlocks[lastMovableOccupied],
                    sep="\n",
                )
                lastMovableOccupied -= 1
                while reorderedBlocks[lastMovableOccupied].isFree:
                    lastMovableOccupied -= 1
            if leftmostFree < lastMovableOccupied:
                reorderedBlocks[leftmostFree], reorderedBlocks[lastMovableOccupied] = (
                    reorderedBlocks[lastMovableOccupied],
                    reorderedBlocks[leftmostFree],
                )
                (
                    reorderedBlocks[leftmostFree].starts,
                    reorderedBlocks[lastMovableOccupied].starts,
                ) = (
                    reorderedBlocks[lastMovableOccupied].starts,
                    reorderedBlocks[leftmostFree].starts,
                )
                while reorderedBlocks[lastMovableOccupied].isFree:
                    lastMovableOccupied -= 1
            leftmostFree = next(freeAscIter)

        self.originalBlocks = reorderedBlocks
        self.layout = self._getLayoutFromBlocks()

    def freeSpaceFragmented(self):
        compactLayout = self._getLayoutFromBlocks()
        lastOccupied = len(compactLayout) - 1
        firstFree = compactLayout.index(".")

        while firstFree < lastOccupied:
            compactLayout[firstFree] = compactLayout[lastOccupied]
            compactLayout[lastOccupied] = "."
            while compactLayout[firstFree] != ".":
                firstFree += 1
            while compactLayout[lastOccupied] == ".":
                lastOccupied -= 1
        self.layout = compactLayout

    @property
    def checksum(self):
        return sum([i * int(val) for i, val in enumerate(self.layout) if val != "."])


if __name__ == "__main__":
    parsedMap = DiskMap.parse(sys.argv[1])
    d = DiskMap(parsedMap)
    print(d)
    d.freeSpaceFragmented()
    print(d)
    print(d.checksum)

    print("=== consecutive ===")
    d = None
    d = DiskMap(parsedMap)
    print(d)
    d.freeSpaceConsecutive()
    print(d)
