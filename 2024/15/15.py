import sys
from pprint import pprint


class Game:

    class GameObj:
        def __init__(self, name, i, j):
            self.name = name
            self.row = i
            self.col = j

        def __repr__(self):
            return f"[{self.row}, {self.col}]: {self.name}"

        @property
        def colend(self):
            return self.col + 1 if self.name == "wbox" else None

        @property
        def gps(self):
            return 100 * self.row + self.col

        def __eq__(self, other):
            if isinstance(other, Game.GameObj):
                return self.name == other.name and self.row == other.row and self.col == other.col
            return NotImplemented

        def __hash__(self):
            return hash((self.name, self.row, self.col))

    DIRS = {">": (0,1), "v": (1,0), "<": (0, -1), "^": (-1, 0)}
    NAMES_TO_REPR = {"wall": "#", "robot": "@", "empty": ".", "box": "O", "wbox": "[]"}

    @staticmethod
    def parseGame(fromfile, widemap: bool):
        vals = []
        actions = []
        parsingGame = True
        with open(fromfile) as f:
            for line in f.readlines():
                cleanedLine = line.strip()
                if cleanedLine == "":
                    parsingGame = False
                    continue
                if parsingGame:
                    if widemap:
                        parsedRow = []
                        for val in cleanedLine:
                            if val == "@":
                                parsedRow.append("@")
                                parsedRow.append(".")
                            elif val == "O":
                                parsedRow.append("[")
                                parsedRow.append("]")
                            else:
                                parsedRow.append(val)
                                parsedRow.append(val)
                        vals.append(parsedRow)
                    else:
                        vals.append([val for val in cleanedLine])

                else:
                    actions.append([action for action in cleanedLine])

        return vals, [a for action in actions for a in action]


    def __init__(self, vals):
        initstate = [[None for _ in vals[0]] for _ in vals]
        for i in range(len(vals)):
            for j in range(len(vals[i])):
                val = vals[i][j]
                if val == "@":
                    robot = Game.GameObj("robot", i, j)
                    initstate[i][j] = robot
                elif val == "#":
                    initstate[i][j] = Game.GameObj("wall", i, j)
                elif val == "O":
                    initstate[i][j] = Game.GameObj("box", i, j)
                elif val == ".":
                    initstate[i][j] = Game.GameObj("empty", i, j)
                elif val == "[":
                    wbox = Game.GameObj("wbox", i, j)
                    initstate[i][j] = wbox
                    initstate[i][j+1] = wbox
                elif val == "]":
                    continue # handled by opening box line
                else:
                    print(f"Fatal, unknown obj found at {i}, {j}: {val}")
                    exit(1)
        self.state = initstate
        self.robot = robot


    def wboxwillmoveto(self, obj, dir):
        if dir in ["<", ">"]:
            return self.willmoveto(obj, dir)

        ni = obj.row + Game.DIRS[dir][0]
        nj = obj.col + Game.DIRS[dir][1]
        nj2 = obj.colend + Game.DIRS[dir][1]
        adjobj1 = self.state[ni][nj]
        adjobj2 = self.state[ni][nj2]
        if adjobj1.name == "empty" and adjobj2.name == "empty":
            return True
        elif adjobj1.name == "wall" or adjobj2.name == "wall":
            return False
        elif adjobj1.name == "robot" or adjobj2.name == "robot":
            print(f"Fatal, robot found at attempted robot move {self.state[ni][nj]}")
            exit(1)

        willmove1 = None
        if adjobj1.name == "wbox":
            willmove1 = self.wboxwillmoveto(adjobj1, dir)
        elif adjobj1.name == "box":
            willmove1 = self.willmoveto(adjobj1, dir)
        elif adjobj1.name == "empty":
            willmove1 = True
        else:
            print(f"Fatal, unknown obj found at {adjobj1}")
            exit(1)

        willmove2 = None
        if adjobj2.name == "wbox":
            willmove2 = self.wboxwillmoveto(adjobj2, dir)
        elif adjobj2.name == "box":
            willmove2 = self.willmoveto(adjobj2, dir)
        elif adjobj2.name == "empty":
            willmove2 = True
        else:
            print(f"Fatal, unknown obj found at {adjobj2}")
            exit(1)

        return willmove1 and willmove2

    def willmoveto(self, obj, dir):
        ni = obj.row + Game.DIRS[dir][0]
        nj = obj.col + Game.DIRS[dir][1]
        if obj.name == "wbox" and dir == ">":
            nj = obj.colend + Game.DIRS[dir][1]
        adjobj = self.state[ni][nj]

        if adjobj.name == "empty":
            return True
        elif adjobj.name == "wall":
            return False
        elif adjobj.name == "box":
            return self.willmoveto(adjobj, dir)
        elif adjobj.name == "wbox":
            return self.wboxwillmoveto(adjobj, dir)
        elif adjobj.name == "robot":
            print(f"Fatal, robot found at attempted robot move {self.state[ni][nj]}")
            exit(1)
        else:
            print(f"Fatal, unknown obj found at {self.state[ni][nj]}")
            exit(1)


    def moveWboxVertically(self, obj, dir):
        if dir in ["<", ">"]:
            print(f"Fatal, this code only handles vertical movement: {obj}, dir={dir}")
            exit(1)

        ni = obj.row + Game.DIRS[dir][0]
        nj = obj.col + Game.DIRS[dir][1]
        nj2 = obj.colend + Game.DIRS[dir][1]
        adjobj1 = self.state[ni][nj]
        adjobj2 = self.state[ni][nj2]
        if adjobj1.name == "wall" or adjobj2.name == "wall":
            print(f"Fatal: what was supposed to be a successful move failed: {obj}, {dir}, {adjobj1}, {adjobj2}, {couldMove1}, {couldMove2}")
            return False
        elif adjobj1.name == "robot" or adjobj2.name == "robot":
            print(f"Fatal, robot found at attempted robot move {self.state[ni][nj]}")
            exit(1)

        shouldMove2 = True
        couldMove1 = None
        if adjobj1.name == "wbox":
            couldMove1 = self.moveWboxVertically(adjobj1, dir)
            if adjobj1.colend == nj:
                self.state[ni][nj-1] = Game.GameObj("empty", ni, nj-1)
            else:
                shouldMove2 = False
        elif adjobj1.name == "box":
            couldMove1 = self.moveObjTo(adjobj1, dir)
        elif adjobj1.name == "empty":
            del adjobj1
            couldMove1 = True
        else:
            print(f"Fatal, unknown obj found at {adjobj1}")
            exit(1)

        if shouldMove2:
            couldMove2 = None
            if adjobj2.name == "wbox":
                couldMove2 = self.moveWboxVertically(adjobj2, dir)
                if adjobj2.col == nj2:
                    self.state[ni][nj2+1] = Game.GameObj("empty", ni, nj2+1)
            elif adjobj2.name == "box":
                couldMove2 = self.moveObjTo(adjobj2, dir)
            elif adjobj2.name == "empty":
                del adjobj2
                couldMove2 = True
            else:
                print(f"Fatal, unknown obj found at {adjobj2}")
                exit(1)

            if not couldMove1 or not couldMove2:
                print(f"Fatal: what was supposed to be a successful move failed: {obj}, {dir}, {adjobj1}, {adjobj2}, {couldMove1}, {couldMove2}")
                exit(1)

        obj.row = ni
        obj.col = nj
        self.state[ni][nj] = obj
        self.state[ni][nj2] = obj
        return True


    def moveObjTo(self, obj, dir):
        if obj.name == "wall":
            print(f"Fatal, wall found at what was supposed to be a successful move {obj}")
            return False
        elif obj.name == "empty":
            del obj
            return True
        elif obj.name == "wbox" and dir in ["^", "v"]:
            couldBeMoved = self.moveWboxVertically(obj, dir)
            return couldBeMoved
        elif obj.name == "box" or obj.name == "robot" or obj.name == "wbox" and dir in ["<", ">"]:
            ni = obj.row + Game.DIRS[dir][0]
            nj = obj.col + Game.DIRS[dir][1]
            if obj.name == "wbox" and dir == ">":
                nj = obj.colend + Game.DIRS[dir][1]
            adjobj = self.state[ni][nj]
            clearOther = None
            if adjobj.name == "wbox" and dir in ["^", "v"]:
                clearOther = nj + 1 if adjobj.col == nj else nj - 1
            couldBeMoved = self.moveObjTo(adjobj, dir)
            if couldBeMoved:
                if obj.name != "wbox":
                    obj.row = ni
                    obj.col = nj
                    self.state[ni][nj] = obj
                    if clearOther:
                        self.state[ni][clearOther] = Game.GameObj("empty", ni, clearOther)
                else: # wbox
                    if dir == "<":
                        obj.row = ni
                        obj.col = nj
                        self.state[ni][nj] = obj
                        self.state[ni][nj+1] = obj
                    else:
                        obj.row = ni
                        obj.col = nj-1
                        self.state[ni][nj-1] = obj
                        self.state[ni][nj] = obj

                return True
        else:
            print(f"Fatal, unknown obj found at {self.state[ni][nj]}")
            exit(1)


    def move(self, dir):
        row = self.robot.row
        col = self.robot.col
        if self.willmoveto(self.robot, dir):
            success = self.moveObjTo(self.robot, dir)
            if not success:
                print("Fatal: a successful move was unsuccessful")
                exit(1)
            self.state[row][col] = Game.GameObj("empty", row, col)

    @property
    def gps(self):
        boxes = set([obj for row in self.state for obj in row if obj.name in ["box", "wbox"]])
        return sum([obj.gps for obj in boxes])

    def __repr__(self):
        l = [[Game.NAMES_TO_REPR[obj.name] for col, obj in enumerate(row) if col == obj.col] for row in self.state]
        s = ""
        for row in l:
            s += "".join(row)
            s += "\n"
        return s


if __name__ == "__main__":
    for isWide in [True]:
        initstate, actions = Game.parseGame(sys.argv[1], isWide)
        g = Game(initstate)
        print(g)
        for i, action in enumerate(actions):
            g.move(action)
            # print(i, action)
            # print(g)

        print(g)
        print(g.gps)

