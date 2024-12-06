from pprint import pprint


def distem(b1, b2):
    b1.sort()
    b2.sort()
    dists = [abs(int(x) - int(y)) for x, y in zip(b1, b2)]
    pprint(sum(dists))


def simem(b1, b2):
    sims = sum([b2.count(x) * int(x) for x in b1])
    print(sims)


with open("in.txt") as f:
    a = [line.split() for line in f.readlines()]
    b1, b2 = [list(x) for x in zip(*a)]
    distem(b1, b2)
    print()
    simem(b1, b2)
