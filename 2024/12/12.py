import sys
from pprint import pprint

# USING GLOBAL IS SUPER UGGLYY!!11! But I don't care.
vals = None

def parseGraph(fromfile):
    global vals
    with open(fromfile) as f:
        content = f.read()

    vals = [[val for val in row] for row in content.split()]
    g = {}
    dirs = [(0,1), (1,0), (0, -1), (-1, 0)]
    inbounds = lambda i, j: i >= 0 and i < len(vals) and j >= 0 and j < len(vals[i])
    for i in range(len(vals)):
        for j in range(len(vals[i])):
            val = vals[i][j]
            v = (i, j, val)
            es = []
            for d in dirs:
                i2 = i + d[0]
                j2 = j + d[1]
                if inbounds(i2,j2) and vals[i2][j2] == val:
                    es.append((i2,j2,vals[i2][j2]))
            g[v] = es
    return g



def getinnercorners(v, edges):
    ne = len(edges)
    diags = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    if ne == 4:
        return sum([v[2] != vals[v[0]+d[0]][v[1]+d[1]] for d in diags])
    elif ne == 2:
        otherrow = edges[0][0] if v[0] == edges[1][0] else edges[1][0]
        othercol = edges[0][1] if v[1] == edges[1][1] else edges[1][1]
        return int(vals[otherrow][othercol] != v[2])
    else: # ne == 3
        rowdiff = edges[0][0] - edges[1][0]
        coldiff = edges[0][1] - edges[1][1]
        if rowdiff == 0 or coldiff == 0:
            return getinnercorners(v, [edges[0], edges[2]]) + getinnercorners(v, edges[1:])
        else:
            rowdiff = edges[1][0] - edges[2][0]
            coldiff = edges[1][1] - edges[2][1]
            if rowdiff == 0 or coldiff == 0:
                return getinnercorners(v, edges[:-1]) + getinnercorners(v, [edges[0], edges[2]])
            else:
                return getinnercorners(v, edges[:-1]) + getinnercorners(v, edges[1:])



def getcorners(v, edges):
    ne = len(edges)
    if ne == 4 or ne == 3:
        return getinnercorners(v, edges)
    elif ne == 1:
        return 2
    elif ne == 0:
        return 4
    else: # ne == 2
        rowdiff = edges[0][0] - edges[1][0]
        coldiff = edges[0][1] - edges[1][1]
        if rowdiff == 0 or coldiff == 0:
            return 0
        else:
            return 1 + getinnercorners(v, edges)



def dfs(g, start, visited):
    if len(g[start]) == 0:
        return 1, 4, 4
    stack = g[start][:]
    area = 0
    perim = 0
    sides = 0
    while stack:
        v = stack.pop()

        if not visited[v]:
            area += 1
            perim += 4 - len(g[v])
            visited[v] = True
            sides += getcorners(v, g[v])
            for u in g[v]:
                stack.append(u)
    return area, perim, sides


if __name__ == "__main__":
    g = parseGraph(sys.argv[1])
    visited = {v: False for v in g}

    areas = []
    perims = []
    sides = []
    for start in g:
        if visited[start]:
            continue
        area, perim, side = dfs(g, start, visited)
        print(start, area, perim, side)
        areas.append(area)
        perims.append(perim)
        sides.append(side)

    print(sum([area * perim for area, perim in zip(areas, perims)]))
    print(sum([area * side for area, side in zip(areas, sides)]))


