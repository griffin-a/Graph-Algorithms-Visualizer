from heapdict import heapdict
from eventmanager import *
"""
This class encapsulates all inner state of the visualizer. 
This includes, application logic and the grid with all of its respective squares
"""
# returns a tuple: (shortest_distance, pred)
import math
from collections import deque
from enum import Enum


WIDTH = HEIGHT = 600


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
                if (i, j) != (self.__x, self.__y) and (0 <= i < WIDTH and 0 < j < HEIGHT):
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

    @property
    def neighbors(self):
        return self.__neighbors

    @neighbors.setter
    def neighbors(self, value):
        self.__neighbors = value


class Model:
    def __init__(self, event_manager):
        # All of type Square
        # When we first initialize the model, we want to set the initial state of all of the squares
        # We want to create a square for each position in the grid
        self.__squares = [Square(x, y) for x in range(WIDTH) for y in range(HEIGHT)]
        self.__start = None
        self.__end = None
        self.__event_manager = event_manager
        self.__event_manager.register_listener(self)
        self.__running = False

    def notify(self, event):
        """
        Called by an event in the message queue.
        """

        if isinstance(event, QuitEvent):
            self.__running = False

    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify().
        """
        self.__running = True
        self.__event_manager.post(InitializeEvent())
        while self.__running:
            new_tick = TickEvent()
            self.__event_manager.post(new_tick)

    def dijkstra(self):
        pq = heapdict()
        pq[self.__start] = 0

        while pq:
            # A tuple is returned, where the fist item is the square and the second value is the priority
            u = pq.popitem()[0]

            for v in u.neighbors:
                cost = math.dist((u.x, u.y), (v.x, v.y))

                if u.distance_from_source + cost < v.distance_from_source:
                    v.distance_from_source = u.distance_from_source + cost
                    v.pred = u
                    pq[v] = v.distance_from_source

                # TODO: Tick update here: one iteration of the algorithm has finished, we now need to update

                if v == self.__end:
                    return v

