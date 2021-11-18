from heapdict import heapdict
import random

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
SQUARE_SIZE = 20


class SquareType(Enum):
    START = 1,
    END = 2,
    WALL = 3,
    NORMAL = 4,
    DONE = 5


class Square:
    def __init__(self, x, y, pred=-1, distance_from_source=float("inf"), square_type=SquareType.NORMAL):
        self.__x = x
        self.__y = y
        self.__distance_from_source = distance_from_source
        self.__neighbors = []
        self.__square_type = square_type
        self.__pred = pred

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

    @property
    def square_type(self):
        return self.__square_type

    @square_type.setter
    def square_type(self, value):
        self.__square_type = value

    # Given an (x,y) coordinate, returns if the coordinate is within the square
    def coordinate_in_square(self, x, y):
        return self.__x <= x <= self.__x + SQUARE_SIZE and self.__y <= y <= self.__y + SQUARE_SIZE

    def __str__(self):
        return f"Square at position: ({self.__x}, {self.__y}) of type: {self.__square_type}"


class Model:
    def __init__(self, event_manager):
        # All of type Square When we first initialize the model, we want to set the initial state of all of the
        # squares We want to create a square for each position in the grid
        # TODO: See if we need to alter each
        #  square's x,y coordinates to make each square at a distance of 1 from each other
        self.__squares = {(x, y): Square(x, y) for x in range(0, WIDTH, SQUARE_SIZE) for y in
                          range(0, HEIGHT, SQUARE_SIZE)}
        self.__start = None
        self.__end = None
        self.__event_manager = event_manager
        self.__event_manager.register_listener(self)
        self.__running = False
        self.state = StateMachine()
        self.shortest_path = []

    def get_neighbors(self, square):
        if square.y - SQUARE_SIZE >= 0:
            square.neighbors.append(self.__squares[(square.x, square.y - SQUARE_SIZE)])
        if square.x - SQUARE_SIZE >= 0:
            square.neighbors.append(self.__squares[(square.x - SQUARE_SIZE, square.y)])
        if square.x + SQUARE_SIZE < WIDTH:
            square.neighbors.append(self.__squares[(square.x + SQUARE_SIZE, square.y)])
        if square.y + SQUARE_SIZE < HEIGHT:
            square.neighbors.append(self.__squares[(square.x, square.y + SQUARE_SIZE)])

        return square.neighbors

    # Go through all of the neighbors in each of the four cardinal directions from the current square
    # Out of the valid neighbors (squares that don't lie outside of the bounds), randomly pick one and return it
    def __get_maze_neighbor(self, square):
        # direction_choice = random.randrange(0, 4)

        # All of the possible neighbors
        neighbors = [(square.x - (2 * SQUARE_SIZE), square.y),
                     (square.x + (2 * SQUARE_SIZE), square.y),
                     (square.x, square.y + (2 * SQUARE_SIZE)),
                     (square.x, square.y - (2 * SQUARE_SIZE))]

        # Remove any of the neighbors that either already visited or lie outside of bounds
        for neighbor in neighbors:
            print(neighbor)
            x, y = neighbor[0], neighbor[1]

            if x < 0 or x > (WIDTH - SQUARE_SIZE):
                neighbors.remove(neighbor)
                print(f"X out of bounds: {x}")
            # We know that the coordinates are valid; now we check if the type is
            if y < 0 or y > (HEIGHT - SQUARE_SIZE):
                neighbors.remove(neighbor)
                print(f"Y out of bounds: {y}")
            # else:
            #     neighbor_square = self.__squares[(x, y)]
            #     if neighbor_square.square_type is not SquareType.WALL:
            #         neighbors.remove(neighbor)

        for neighbor in neighbors:
            neighbor_square = self.__squares[neighbor]
            if neighbor_square.square_type is not SquareType.WALL:
                neighbors.remove(neighbor)

        # print(neighbors)
        # Out of the remaining valid neighbors, randomly select and return one
        random_index = random.randrange(0, len(neighbors))
        coordinates = neighbors[random_index]
        # print(coordinates)
        return self.__squares[coordinates]

    # Using randomized DFS to generate a maze
    def generate_maze(self):
        # Initialize all squares to walls
        for square in self.__squares.values():
            square.square_type = SquareType.WALL

        stack = []

        # Pick a random node to make normal
        rand_x, rand_y = random.randrange(0, WIDTH - SQUARE_SIZE, SQUARE_SIZE), random.randrange(0,
                                                                                                 HEIGHT - SQUARE_SIZE,
                                                                                                 SQUARE_SIZE)

        rand_square = self.__squares[(rand_x, rand_y)]
        rand_square.square_type = SquareType.NORMAL

        # Append the first chosen node into the stack
        stack.append(rand_square)

        iteration = 0

        while stack:
            iteration += 1
            # print(iteration)

            # Pop a node from the stack
            current = stack.pop()
            # print(current)

            # Now we need to get an unvisited neighbor (if there are any)
            chosen_neighbor = self.__get_maze_neighbor(current)

            if chosen_neighbor:
                # while 0 <= neighbors[direction_choice].x < WIDTH and 0 <= neighbors[direction_choice].y < HEIGHT \
                #         and neighbors[direction_choice].square_type is not SquareType.WALL:
                #     direction_choice = random.randrange(0, 4)

                # print(chosen_neighbor)
                chosen_neighbor.square_type = SquareType.NORMAL

                # find the midpoint between the current square and chosen neighbor
                midpoint = ((current.x + chosen_neighbor.x) // 2, (current.y + chosen_neighbor.y) // 2)
                midpoint_square = self.__squares[midpoint]
                midpoint_square.square_type = SquareType.NORMAL

                self.__event_manager.post(TickEvent())

                stack.append(chosen_neighbor)

    def notify(self, event):
        """
        Called by an event in the message queue.
        """

        if isinstance(event, QuitEvent):
            self.__running = False
        if isinstance(event, StateChangeEvent):
            # pop request
            if not event.state:
                # false if no more states are left
                if not self.state.pop():
                    self.__event_manager.post(QuitEvent())
            else:
                # push a new state on the stack
                self.state.push(event.state)

        if isinstance(event, InputEvent):
            # We now need to determine which squares were clicked on to set start and end
            if event.char == "maze":
                self.generate_maze()
                self.__event_manager.post(TickEvent())
            elif event.char == "left_click" or event.char == "right_click":
                clickpos = event.clickpos

                if clickpos:
                    # Setting the start here
                    if event.char == "left_click":
                        # Now we search all of the squares to see which square was clicked on
                        if not self.__start:
                            for square in self.__squares.values():
                                if square.coordinate_in_square(clickpos[0], clickpos[1]):
                                    # set the square to be the start square Now that we have picked a start square,
                                    # we have to prevent the user from picking another start
                                    # TODO: consider adding a new
                                    #  state to prevent this from happening? Only allowing end square input
                                    square.square_type = SquareType.START
                                    square.distance_from_source = 0
                                    self.get_neighbors(square)
                                    self.__start = square
                                    print(self.__start)
                                    print(square.neighbors)
                                    break
                            # Post the start square to the view observer of model
                            self.__event_manager.post(TickEvent("start", self.__start))
                        else:
                            for square in self.__squares.values():
                                if square.coordinate_in_square(clickpos[0], clickpos[1]):
                                    square.square_type = SquareType.WALL
                                    break
                            self.__event_manager.post(TickEvent())

                    elif event.char == "right_click":
                        # Post the end square to the view observer of model
                        print("right click in model")
                        for square in self.__squares.values():
                            if square.coordinate_in_square(clickpos[0], clickpos[1]):
                                square.square_type = SquareType.END
                                self.get_neighbors(square)
                                self.__end = square
                                print(self.__end)
                                print(square.neighbors)
                                break
                        self.__event_manager.post(TickEvent("end", self.__end))

    def run(self):
        """
        Starts the game engine loop.

        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify().
        """
        self.__running = True
        self.__event_manager.post(InitializeEvent())
        self.state.push(StateType.SELECTION)
        while self.__running:
            if self.state.peek() == StateType.RUNNING and not self.state.peek() == StateType.ENDED:
                # Run the algorithm, all the while, posting new events when appropriate
                self.dijkstra()
            elif self.state.peek() == StateType.SELECTION:
                new_tick = TickEvent(self.__squares)
                self.__event_manager.post(new_tick)
            elif self.state.peek() == StateType.ENDED:
                new_tick = TickEvent(self.shortest_path)
                self.__event_manager.post(new_tick)

    def dijkstra(self):
        pq = heapdict()
        pq[self.__start] = 0

        while pq:
            # A tuple is returned, where the fist item is the square and the second value is the priority
            u = pq.popitem()[0]
            # print(f"u: {u}")

            for v in self.get_neighbors(u):
                # print(f"v: {v}")

                if v.square_type is SquareType.NORMAL or v.square_type is SquareType.END:
                    cost = math.dist((u.x, u.y), (v.x, v.y))

                    if u.distance_from_source + cost < v.distance_from_source:
                        v.distance_from_source = u.distance_from_source + cost
                        v.pred = u
                        if v.square_type is not SquareType.END:
                            v.square_type = SquareType.DONE

                        pq[v] = v.distance_from_source

                    # TODO: Tick update here: one iteration of the algorithm has finished, we now need to update
                    # We want to encapsulate the entire grid and priority queue to be able to draw the updated state
                    new_tick = TickEvent((self.__squares, pq))
                    self.__event_manager.post(new_tick)

                if v == self.__end or v.square_type is SquareType.END:
                    # TODO: Notify all listeners that the algorithm has terminated and post the shortest path in the
                    #  event
                    self.shortest_path = self.get_shortest_path(v)
                    print(self.shortest_path)
                    self.__event_manager.post(StateChangeEvent(StateType.ENDED))
                    return v

    def get_shortest_path(self, square):
        current_square = self.__end
        path = []

        while current_square.pred != -1:
            path.append(current_square)
            current_square = current_square.pred

        return path

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, value):
        self.__start = value

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, value):
        self.__end = value

    @property
    def squares(self):
        return self.__squares

    @squares.setter
    def squares(self, value):
        self.__squares = value


class StateType(Enum):
    # The user has yet to select the start and end squares and press start
    SELECTION = 1,
    # The user has picked the start and end, now they can generate walls if they wish
    WALL = 5,
    # The simulation is running
    RUNNING = 2,
    # The simulation is paused
    PAUSED = 3,
    # The simulation has ended
    ENDED = 4


class StateMachine:
    def __init__(self):
        self.__state_stack = []

    def peek(self):
        """
        Returns the current state without altering the stack.
        Returns None if the stack is empty.
        """
        try:
            return self.__state_stack[-1]
        except IndexError:
            # empty stack
            return None

    def pop(self):
        """
        Returns the current state and remove it from the stack.
        Returns None if the stack is empty.
        """
        try:
            self.__state_stack.pop()
            return len(self.__state_stack) > 0
        except IndexError:
            # empty stack
            return None

    def push(self, state):
        """
        Push a new state onto the stack.
        Returns the pushed value.
        """
        self.__state_stack.append(state)
        return state
