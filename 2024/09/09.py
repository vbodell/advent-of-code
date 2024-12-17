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
        l = ["." for _ in range(self.totalSize)]
        layoutNdx = 0
        for ndx, size in enumerate(self.originalMap):
            isFree = ndx % 2
            filen = ndx // 2
            icon = str(filen)
            if not isFree:
                for ln in range(layoutNdx, layoutNdx + size):
                    l[ln] = icon
            layoutNdx += size
        return l

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
        while consecutiveLayout[lastOccupied] == ".":
            lastOccupied -= 1
        leftmostFree = consecutiveLayout.index(".")

        while lastOccupied > 0:
            if (
                lastOccupied < leftmostFree
            ):  # scanned files past current freespace, attempt to look for freespace from start of disk
                leftmostFree = consecutiveLayout.index(".")
                if lastOccupied < leftmostFree:
                    break

            freeSize = DiskMap.getFreeSizeAscending(consecutiveLayout, leftmostFree)
            filesize = DiskMap.getFileSizeDescending(consecutiveLayout, lastOccupied)
            # print("start", leftmostFree, lastOccupied, freeSize, filesize)
            while filesize > freeSize:
                # skip to next freespace
                # print("toobig", leftmostFree, lastOccupied, freeSize, filesize)
                leftmostFree += freeSize
                while (
                    consecutiveLayout[leftmostFree] != "."
                    and leftmostFree < lastOccupied
                ):
                    leftmostFree += 1

                if leftmostFree >= lastOccupied:

                    # print("passed", leftmostFree, lastOccupied, freeSize, filesize)
                    break

                freeSize = DiskMap.getFreeSizeAscending(consecutiveLayout, leftmostFree)

            if (
                not leftmostFree >= lastOccupied
            ):  # swap disk and move pointers if we didnt scan past current freespace
                # print("swap", leftmostFree, lastOccupied, freeSize, filesize)

                DiskMap.swapMem(consecutiveLayout, leftmostFree, lastOccupied, filesize)
                leftmostFree = consecutiveLayout.index(".")

            # print("goto-next-file", leftmostFree, lastOccupied, freeSize, filesize)
            lastOccupied -= filesize
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
        numvals = [int(val) if val != "." else 0 for val in self.layout]
        return sum([i * val for i, val in enumerate(numvals)])


if __name__ == "__main__":
    parsedMap = DiskMap.parse(sys.argv[1])
    d = DiskMap(parsedMap)
    # print(d)
    # d.freeSpaceFragmented()
    # print(d)
    # print(d.checksum)

    # d.reset()
    print(d.totalSize)
    # print(d)
    d.freeSpaceConsecutive()
    # print(d)
    print(d.checksum)
