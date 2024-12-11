import sys

class Stone:
    def __init__(self, value, prev):
        self.value = value
        self.next = None
        self.prev = prev

    def tick(self):
        if self.value == 0:
            self.value = 1
        elif len(str(self.value)) % 2 == 0:
            ls = self.split()
            return True, ls
        else:
            self.value *= 2024
        return False, None

    def split(self):
        s = str(self.value)
        lhs, rhs = s[:len(s)//2], s[len(s)//2:]
        ls = Stone(int(lhs), self.prev)
        rs = Stone(int(rhs), ls)
        if self.prev is not None:
            self.prev.next = ls
        ls.next = rs
        if self.next is not None:
            self.next.prev = rs
        rs.next = self.next
        return ls


class Stones:
    def __init__(self, fn):
        with open(fn) as f:
            vals = f.read().split()

        self.root = None

        prev = None
        for val in vals:
            s = Stone(int(val), prev)
            if prev is None:
                self.root = s
            else:
                prev.next = s
            prev = s

    def size(self):
        sz = 0
        n = self.root
        while n is not None:
            sz += 1
            n = n.next
        return sz

    def tick(self):
        n = self.root
        isroot = True
        while n is not None:
            wasSplit, new = n.tick()
            if wasSplit:
                n = new.next.next
                if isroot:
                    self.root = new
            else:
                n = n.next
            isroot = False

    def __repr__(self):
        l = []
        n = self.root
        while n is not None:
            l.append(str(n.value))
            n = n.next
        return " ".join(l)

if __name__ == "__main__":
    ss = Stones(sys.argv[1])
    print(ss)

    ticks = int(sys.argv[2])
    for i in range(ticks):
        ss.tick()
        print(i)
    print(ss.size())
