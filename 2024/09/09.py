import sys


class DiskMap:
    @staticmethod
    def parse(filename):
        with open(filename) as f:
            line = f.read()
        return [int(x) for x in line.strip()]

    def __init__(self, map):
        self.originalMap = map
        self.totalSize = sum(map)
        self.layout = self._getOriginalLayout()

    def _getOriginalLayout(self):
        l = []
        layoutNdx = 0
        for ndx, size in enumerate(self.originalMap):
            isFree = ndx % 2
            filen = ndx // 2
            icon = str(filen) if not isFree else "."
            l.append(list(icon * size))
            layoutNdx += size
        return [x for iconl in l for x in iconl]

    def __repr__(self):
        return "".join(self.layout)

    def reset(self):
        self.layout = self._getOriginalLayout()

    @staticmethod
    def getFreeSizeAscending(l, start):
        size = 0
        while l[start] == ".":
            start += 1
            size += 1
        return size

    @staticmethod
    def getFileSizeDescending(l, end):
        size = 0
        filen = l[end]
        while l[end] == filen:
            end -= 1
            size += 1
        return size

    @staticmethod
    def swapMem(l, start, end, size):
        while size:
            l[start], l[end] = l[end], l[start]
            start += 1
            end -= 1
            size -= 1

    def freeSpaceConsecutive(self):
        consecutiveLayout = self.layout[:]
        lastOccupied = len(consecutiveLayout) - 1
        leftmostFree = consecutiveLayout.index(".")

        while lastOccupied > 0:
            print("start", leftmostFree, lastOccupied, sep="\n")
            if (
                lastOccupied < leftmostFree
            ):  # scanned files past current freespace, attempt to look for freespace from start of disk
                leftmostFree = consecutiveLayout.index(".")
                if lastOccupied < leftmostFree:
                    break

            freeSize = DiskMap.getFreeSizeAscending(consecutiveLayout, leftmostFree)
            filesize = DiskMap.getFileSizeDescending(consecutiveLayout, lastOccupied)
            while filesize > freeSize:
                print("toobig", leftmostFree, lastOccupied, sep="\n")
                # skip to next file
                lastOccupied -= filesize
                while consecutiveLayout[lastOccupied] == ".":
                    lastOccupied -= 1
                filesize = DiskMap.getFileSizeDescending(
                    consecutiveLayout, lastOccupied
                )

            print("not-toobig", leftmostFree, lastOccupied, sep="\n")
            if (
                not lastOccupied < leftmostFree
            ):  # swap disk and move pointers if we didnt scan past current freespace
                print("swapping", leftmostFree, lastOccupied, sep="\n")
                DiskMap.swapMem(consecutiveLayout, leftmostFree, lastOccupied, filesize)
                leftmostFree += (
                    freesize  # unclear if should skip past freesize but let's
                )
                lastOccupied -= filesize
                while consecutiveLayout[leftmostFree] != ".":
                    leftmostFree += 1
                while consecutiveLayout[lastOccupied] == ".":
                    lastOccupied -= 1

        self.layout = consecutiveLayout

    def freeSpaceFragmented(self):
        compactLayout = self.layout[:]
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
    d.reset()
    print(d)
    d.freeSpaceConsecutive()
    print(d)
