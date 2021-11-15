import heapq
import math
from collections import deque
from enum import Enum

import pygame


class Square:
    class SquareType(Enum):
        START = 1,
        END = 2,
        WALL = 3,
        NORMAL = 4

    def __init__(self, x, y, square_type=SquareType.NORMAL):
        self.x = x
        self.y = y
        self.square_type = square_type

    def get_neighbors(self, width, height):
        adj = set()

        # # upper bound in range is exclusive not inclusive
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if (i, j) != (self.x, self.y) and (0 <= i < width and 0 < j < height):
                    adj.add((i, j))

        return adj


def dijkstra_modified(source, dest, width, height):
    done = set()
    pq = []
    distance = {(x, y): float("inf") for x in range(width) for y in range(height)}
    is_wall = {(x, y): False for x in range(width) for y in range(height)}
    distance[source] = 0
    heapq.heappush(pq, (distance[source], source))
    pred = {(x, y): -1 for x in range(width) for y in range(height)}

    while pq:
        u = heapq.heappop(pq)
        neighbors = get_neighbors(u, width, height)

        if u not in done:
            done.add(u)

            for v in neighbors:
                cost = math.dist(u[1], v)

                if distance[u[1]] + cost < distance[v]:
                    distance[v] = distance[u[1]] + cost
                    pred[v] = u[1]

                    if v not in done:
                        heapq.heappush(pq, (distance[v], v))

                if v == dest:
                    print("Reached destination")
                    return distance[dest], pred


def get_shortest_path(pred, source, dest):
    # Backtrack from the dest node to the source node to get the shortest path
    path = deque()
    temp_pred = pred[dest]
    path.appendleft(dest)

    while temp_pred != -1:
        path.appendleft(temp_pred)
        temp_pred = pred[temp_pred]

    return path


def main():
    pass
