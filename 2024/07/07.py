import sys
from pprint import pprint
from tqdm import tqdm


class Combination:
    def __init__(self, result, vals):
        self.result = result
        self.vals = vals
        self.ops = None
        self.opsLength = len(vals) - 1

    def setOps(self, ops):
        self.ops = ops

    def eval(self):
        for opslist in self.ops:
            running = self.vals[0]
            for val, op in zip(self.vals[1:], opslist):
                running = op(running, val)
            if running == self.result:
                return True
        return False

    def __repr__(self):
        return f"r={self.result}, v={self.vals}\n\to={self.ops}"


class Combos:
    @staticmethod
    def _parseFile(filename):
        combos = []
        with open(filename) as f:
            for line in f.readlines():
                [result, vals] = line.split(":")
                vals = [int(val) for val in vals.split()]
                combination = Combination(int(result), vals)
                combos.append(combination)
        return combos

    def __init__(self, filename, ops):
        self.combos = self._parseFile(filename)
        maxNumberOfOps = max([len(c.vals) for c in self.combos]) - 1
        self.ops = ops
        self.opsCombos = self._calcOpsCombos(maxNumberOfOps)
        for combo in self.combos:
            combo.setOps(self.opsCombos[combo.opsLength])

    def _getCombosFor(self, numberOfOps):
        opsToChooseFrom = len(self.ops)
        lists = len(self.ops) ** numberOfOps
        res = []
        for ndx in range(lists):
            indices = []
            while ndx > 0:
                indices.append(ndx % opsToChooseFrom)
                ndx //= opsToChooseFrom
            indices.reverse()
            leadingZeros = [0 for _ in range(numberOfOps - len(indices))]
            # print(numberOfOps, leadingZeros, indices)
            indices = leadingZeros + indices
            res.append([self.ops[i] for i in indices])
        return res

    def _calcOpsCombos(self, maxNumberOfOps):
        opsdict = {}
        numberOfOps = len(self.ops)

        for k in range(1, maxNumberOfOps + 1):
            opsdict[k] = self._getCombosFor(k)

        return opsdict

    def __str__(self):
        return "\n".join([str(c) for c in self.combos])

    def getValidCombos(self):
        res = []
        for c in tqdm(self.combos):
            if c.eval():
                res.append(c)
        return res


class Op:
    def __init__(self, name, op):
        self.name = name
        self.op = op

    def __repr__(self):
        return self.name

    def __call__(self, *args):
        return self.op(*args)


def numberConcat(x, y):
    oy = y
    while y > 0:
        x *= 10
        y //= 10
    return x + oy


if __name__ == "__main__":
    add = Op("add", lambda x, y: x + y)
    mul = Op("mul", lambda x, y: x * y)
    concat = Op("concat", lambda x, y: int(str(x) + str(y)))
    # concat = Op("concat", numberConcat)
    ops = [add, mul, concat]
    c = Combos(sys.argv[1], ops)
    validcs = c.getValidCombos()
    print(sum(c.result for c in validcs))
