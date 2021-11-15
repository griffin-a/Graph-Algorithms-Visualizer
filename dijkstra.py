from heapdict import heapdict

# returns a tuple: (shortest_distance, pred)
import math
from collections import deque
from enum import Enum

from view_controller import ViewController


class SquareType(Enum):
    START = 1,
    END = 2,
    WALL = 3,
    NORMAL = 4


class Square:
    def __init__(self, x, y, pred=-1, distance_from_source=float("inf"), square_type=SquareType.NORMAL):
        self.__x = x
        self.__y = y
        self.__distance_from_source = distance_from_source
        self.__neighbors = []
        self.__square_type = square_type
        self.__pred = pred

    def get_neighbors(self):
        # # upper bound in range is exclusive not inclusive
        for i in range(self.__x - 1, self.__x + 2):
            for j in range(self.__y - 1, self.__y + 2):
                if (i, j) != (self.__x, self.__y) and (0 <= i < ViewController.width and 0 < j < ViewController.height):
                    self.__neighbors.append((i, j))

    @property
    def square_type(self):
        return self.__square_type

    @square_type.setter
    def square_type(self, value):
        self.__square_type = value

    @property
    def distance_from_source(self):
        return self.__distance_from_source

    @distance_from_source.setter
    def distance_from_source(self, value):
        self.__distance_from_source = value

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def pred(self):
        return self.__pred

    @pred.setter
    def pred(self, value):
        self.__pred = value


class Model:
    def __init__(self, view_controller):
        self.__view_controller = view_controller

        # All of type Square
        self.__squares = []
        self.__start = None
        self.__end = None

    # Called in view-controller
    def dijkstra(self, start, end, width, height):
        done = set()
        pq = heapdict()
        start_square = Square(start[0], start[1], -1, 0, SquareType.START)
        pq[start_square] = 0

    # def dijkstra_modified(self, source, dest, width, height):
    #     done = set()
    #     pq = []
    #     distance = {(x, y): float("inf") for x in range(width) for y in range(height)}
    #     is_wall = {(x, y): False for x in range(width) for y in range(height)}
    #     distance[source] = 0
    #     heapq.heappush(pq, (distance[source], source))
    #     pred = {(x, y): -1 for x in range(width) for y in range(height)}
    #
    #     while pq:
    #         u = heapq.heappop(pq)
    #         neighbors = get_neighbors(u, width, height)
    #
    #         if u not in done:
    #             done.add(u)
    #
    #             for v in neighbors:
    #                 cost = math.dist(u[1], v)
    #
    #                 if distance[u[1]] + cost < distance[v]:
    #                     distance[v] = distance[u[1]] + cost
    #                     pred[v] = u[1]
    #
    #                     if v not in done:
    #                         heapq.heappush(pq, (distance[v], v))
    #
    #                 if v == dest:
    #                     print("Reached destination")
    #                     return distance[dest], pred
    #
    # # Prints out the nodes that are taken on the shortest path from source to dest
    # def get_shortest_path(pred, source, dest):
    #     # Backtrack from the dest node to the source node to get the shortest path
    #     path = deque()
    #     temp_pred = pred[dest]
    #     path.appendleft(dest)
    #
    #     while temp_pred != -1:
    #         path.appendleft(temp_pred)
    #         temp_pred = pred[temp_pred]
    #
    #     return path
