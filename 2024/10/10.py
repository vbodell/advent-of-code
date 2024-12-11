import sys
import heapq


class MinPQ:
    def __init__(self):
        self.heap = []  # Internal list to store heap elements
        self.entry_finder = {}  # Map of items to their heap entries

    def push(self, item, priority):
        """
        Add an item with its priority to the queue.
        If the item already exists, replace its priority.
        """
        if item in self.entry_finder:
            self.decrease_priority(item, priority)
            return
        entry = [priority, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.heap, entry)

    def pop(self):
        """
        Remove and return the item with the lowest priority.
        """
        while self.heap:
            priority, item = heapq.heappop(self.heap)
            if item in self.entry_finder and self.entry_finder[item] == [priority, item]:
                del self.entry_finder[item]
                return item
        raise IndexError("pop from an empty priority queue")

    def peek(self):
        """
        Peek at the item with the lowest priority without removing it.
        """
        while self.heap:
            priority, item = self.heap[0]
            if item in self.entry_finder and self.entry_finder[item] == [priority, item]:
                return item
            heapq.heappop(self.heap)  # Remove invalid entries
        raise IndexError("peek from an empty priority queue")

    def is_empty(self):
        """
        Check if the queue is empty.
        """
        return len(self.entry_finder) == 0

    def size(self):
        """
        Return the number of items in the queue.
        """
        return len(self.entry_finder)

    def decrease_priority(self, item, new_priority):
        """
        Decrease the priority of an existing item.
        """
        if item not in self.entry_finder:
            raise KeyError(f"Item '{item}' not found in the queue")
        old_entry = self.entry_finder[item]
        if new_priority >= old_entry[0]:
            raise ValueError("New priority must be lower than the current priority")
        # Remove old entry and push new one
        self.entry_finder[item] = [new_priority, item]
        heapq.heappush(self.heap, [new_priority, item])


def parseGraph(fromfile):
    with open(fromfile) as f:
        content = f.read()

    vals = [[int(val) if val != '.' else 100 for val in row] for row in content.split()]
    g = {}
    dirs = [(0,1), (1,0), (0, -1), (-1, 0)]
    inbounds = lambda i, j: i >= 0 and i < len(vals) and j >= 0 and j < len(vals[i])

    for i in range(len(vals)):
        for j in range(len(vals[i])):
            v = (i, j, vals[i][j])
            es = []
            for d in dirs:
                i2 = i + d[0]
                j2 = j + d[1]
                if inbounds(i2,j2) and vals[i2][j2] - v[2] == 1:
                    es.append((i2,j2,vals[i2][j2]))
            g[v] = es
    return g


def dijkstra(g, source):
    dists = {v: float('inf') for v in g}
    prev = {v: [] for v in g}
    q = MinPQ()
    for v in g:
        if v != source:
            q.push(v, float('inf'))
    dists[source] = 0
    q.push(source, 0)

    while not q.is_empty():
        u = q.pop()

        for v in g[u]:
            alt = dists[u] + 1
            if alt < dists[v]:
                dists[v] = dists[u] + 1
                prev[v].append(u)
                q.push(v, dists[u]+1)
            elif alt == dists[v]:
                prev[v].append(u)

    return dists, prev


def dfs(g, start):
    stack = g[start][:]
    visited = {v: False for v in g}
    roots = 0
    while stack:
        v = stack.pop()
        if v[2] == 0:
            roots += 1
        for u in g[v]:
            stack.append(u)
    return roots


if __name__ == "__main__":
    g = parseGraph(sys.argv[1])
    sources = [v for v in g if v[2] == 0]

    d = {}
    scores = []
    ratings = []
    for source in sources:
        dists, prevs = dijkstra(g, source)
        d[source] = (dists, prevs)
        targets = [d for d in dists if d[2] == 9 and dists[d] < float('inf')]
        scores.append(len(targets))
        for target in targets:
            ratings.append(dfs(prevs, target))

    print(sum(scores))
    print(sum(ratings))


