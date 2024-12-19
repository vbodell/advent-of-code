from pprint import pprint
import sys

def parseEqs(filename):
    with open(filename) as f:
        content = f.read()

    eqs = []
    eq = {}
    for line in content.split("\n"):
        if line.strip() == "":
            eq = {}
            continue
        key = line.split(":")[0]
        x, y = line.split(":")[1].split(",")
        if "Button" in key:
            xkey, xval = x.split("+")
            ykey, yval = y.split("+")
            eq[key[-1]] = {}
            eq[key[-1]][xkey.strip()] = int(xval)
            eq[key[-1]][ykey.strip()] = int(yval)
        else:
            xkey, xval = x.split("=")
            ykey, yval = y.split("=")
            eq[key[0]] = {}
            eq[key[0]][xkey.strip()] = int(xval)
            eq[key[0]][ykey.strip()] = int(yval)
        eqs.append(eq)
    return eqs

def solveEq(A, B, P):
    # eq1: eq["A"]["X"] * A + eq["B"]["X"] * B - eq["Prize"]["X"] == 0
    # eq2: eq["A"]["Y"] * A + eq["B"]["Y"] * B - eq["Prize"]["Y"] == 0
    # eq1 - eq2: A * (eq["A"]["X"] - eq["A"]["Y"]) + B * (eq["B"]["X"] - eq["B"]["Y"]) - eq["Prize"]["X"] + eq["Prize"]["Y"] == 0
    # BinA: B = (eq["Prize"]["X"] - eq["Prize"]["Y"] - A * (eq["A"]["X"] - eq["A"]["Y"]))/(eq["B"]["X"] - eq["B"]["Y"])

    # 3 * A + B == cost
    # BinA for eq1: eq["A"]["X"] * A + eq["B"]["X"] * (eq["Prize"]["X"] - eq["Prize"]["Y"] - A * (eq["A"]["X"] - eq["A"]["Y"]))/(eq["B"]["X"] - eq["B"]["Y"]) - eq["Prize"]["X"] == 0
    # P["X"] * (B["X"] + B["Y"]) - B["X"] * P["X"] + B["X"] * P["Y"]  == A * A["X"]  - A * B["X"] * A["X"] + A * B["X"] * A["Y"]
    # A = lhs / (A["X"] - B["X"] * A["X"] + B["X"] * A["Y"])

    quot = (P["X"] * (B["X"] + B["Y"]) - B["X"] * P["X"] + B["X"] * P["Y"])
    denom = (A["X"] - B["X"] * A["X"] + B["X"] * A["Y"]) 
    print(quot, denom, quot / denom)
    if quot % denom != 0:
        return 0

    A = quot // denom
    quot = (P["X"] - P["Y"] - A * (A["X"] - A["Y"]))
    denom = (B["X"] - B["Y"])
    print(quot, denom, quot / denom)
    if quot % denom != 0:
        return 0
    B = quot // denom

    return 3 * A + B

if __name__ == "__main__":
    eqs = parseEqs(sys.argv[1])
    pprint(eqs)
    eq = eqs[0]
    print(eq)
    solveEq(eq["A"], eq["B"], eq["P"])
