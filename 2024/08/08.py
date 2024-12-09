import sys
from pprint import pprint


class Map:
    def __init__(self, filename):
        self.map = Map.parse_from_file(filename)
        self.antennas = Map.group_antennas(self.map)
        self.antinodes = None

    @staticmethod
    def parse_from_file(filename):
        with open(filename) as f:
            content = f.read()
        return [list(x) for x in content.split()]

    @staticmethod
    def group_antennas(a_map):
        symbols = set([point for row in a_map for point in row])
        antennas = {s: [] for s in symbols if s != "."}
        for i, row in enumerate(a_map):
            for j, loc in enumerate(row):
                if loc != ".":
                    antennas[loc].append((i, j))
        return antennas

    def inbounds(self, i, j):
        return i >= 0 and i < len(self.map) and j >= 0 and j < len(self.map[i])

    def find_antinodes_with_resonant_harmonics(self):
        antinodes = {freq: [] for freq in self.antennas}
        for freq in self.antennas:
            for a1, a2 in nck(self.antennas[freq], 2):
                disti = a2[0] - a1[0]
                distj = a2[1] - a1[1]
                cand1 = a1
                cand2 = a2
                while self.inbounds(*cand1):
                    antinodes[freq].append(cand1)
                    cand1 = (cand1[0] - disti, cand1[1] - distj)
                while self.inbounds(*cand2):
                    antinodes[freq].append(cand2)
                    cand2 = (cand2[0] + disti, cand2[1] + distj)
        self.antinodes = antinodes

    def find_antinodes(self):
        antinodes = {freq: [] for freq in self.antennas}
        for freq in self.antennas:
            for a1, a2 in nck(self.antennas[freq], 2):
                disti = a2[0] - a1[0]
                distj = a2[1] - a1[1]
                cand1 = (a1[0] - disti, a1[1] - distj)
                cand2 = (a2[0] + disti, a2[1] + distj)
                if self.inbounds(*cand1):
                    antinodes[freq].append(cand1)
                if self.inbounds(*cand2):
                    antinodes[freq].append(cand2)
        self.antinodes = antinodes

    def get_unique_antinodes(self):
        if self.antinodes is None:
            return 0
        return len(
            set(
                [
                    a
                    for freq_antinodes in self.antinodes.values()
                    for a in freq_antinodes
                ]
            )
        )

    def draw(self, with_antinodes=False):
        map_to_draw = self.map
        if with_antinodes and self.antinodes is not None:
            antinodes = [
                a for freq_antinodes in self.antinodes.values() for a in freq_antinodes
            ]
            for i, j in antinodes:
                map_to_draw[i][j] = "#"

        s = ""
        for row in map_to_draw:
            s += "".join(row) + "\n"
        print(s)

    def __repr__(self):
        s = f"{self.antennas}\n"
        for row in self.map:
            s += "".join(row) + "\n"
        return s


def nck(n, k):
    # Choose k elements from bag of n. Returns all permutations of n choose k
    # irrespective of order, i.e. elements a and b only gets returned in one
    # sequence, where the first element is the first to appear in the sequence.
    # Except right now this only choses 2 elements...
    return [[e1, e2] for i, e1 in enumerate(n[:-1]) for e2 in n[i + 1 :]]


if __name__ == "__main__":
    m = Map(sys.argv[1])
    m.draw()
    m.find_antinodes()
    m.draw(True)
    print(m.get_unique_antinodes())
    m.find_antinodes_with_resonant_harmonics()
    m.draw(True)
    print(m.get_unique_antinodes())
