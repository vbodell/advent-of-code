import sys
from pprint import pprint
from collections import defaultdict

def get_stones(fn):
    with open(fn) as f:
        vals = f.read().split()

    stones = defaultdict(int)
    for stone in vals:
        stones[int(stone)] += 1
    return stones


def tickstone(stone, amount, stones):
    if stone == 0:
        stones[1] += amount
    elif len(str(stone)) % 2 == 0:
        left = str(stone)[len(str(stone))//2:]
        right = str(stone)[:len(str(stone))//2]
        stones[int(left)] += amount
        stones[int(right)] += amount
    else:
        newstone = stone * 2024
        stones[newstone] += amount


def tick(stones):
    nextgen = defaultdict(int)
    [tickstone(stone, stones[stone], nextgen) for stone in stones]
    return nextgen


if __name__ == "__main__":
    ss = get_stones(sys.argv[1])
    pprint(ss)

    ticks = int(sys.argv[2])
    for i in range(int(ticks)):
        ss = tick(ss)
    pprint(ss)
    print(sum(ss.values()))
