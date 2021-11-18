import pygame

from heapdict import heapdict
import random
import math
from enum import Enum

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

"""
This class encapsulates all inner state of the visualizer. 
This includes, application logic and the grid with all of its respective squares
"""
WIDTH = HEIGHT = 600
SQUARE_SIZE = 20


class SquareType(Enum):
    START = 1,
    END = 2,
    WALL = 3,
    NORMAL = 4,
    DONE = 5


class ClickOperation(Enum):
    SET_START = 1,
    SET_END = 2,
    SET_WALL = 3
    DELETE = 4


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
    def __init__(self):
        # All of type Square When we first initialize the model, we want to set the initial state of all of the
        # squares We want to create a square for each position in the grid
        # TODO: See if we need to alter each
        #  square's x,y coordinates to make each square at a distance of 1 from each other
        self.__squares = {(x, y): Square(x, y) for x in range(0, WIDTH, SQUARE_SIZE) for y in
                          range(0, HEIGHT, SQUARE_SIZE)}
        self.__start = None
        self.__end = None
        self.__running = False
        self.shortest_path = []

    def handle_click(self, click_pos, click_state, draw):
        x, y = click_pos[0], click_pos[1]

        for square in self.__squares.values():
            if square.coordinate_in_square(x, y):
                if click_state is ClickOperation.SET_START:
                    square.square_type = SquareType.START
                    self.__start = square
                    draw()
                elif click_state is ClickOperation.SET_END:
                    square.square_type = SquareType.END
                    self.__end = square
                    draw()
                elif click_state is ClickOperation.SET_WALL:
                    square.square_type = SquareType.WALL
                    draw()

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

    # # Go through all of the neighbors in each of the four cardinal directions from the current square
    # # Out of the valid neighbors (squares that don't lie outside of the bounds), randomly pick one and return it
    # def __get_maze_neighbor(self, square):
    #     # direction_choice = random.randrange(0, 4)
    #
    #     # All of the possible neighbors
    #     neighbors = [(square.x - (2 * SQUARE_SIZE), square.y),
    #                  (square.x + (2 * SQUARE_SIZE), square.y),
    #                  (square.x, square.y + (2 * SQUARE_SIZE)),
    #                  (square.x, square.y - (2 * SQUARE_SIZE))]
    #
    #     # Remove any of the neighbors that either already visited or lie outside of bounds
    #     for neighbor in neighbors:
    #         print(neighbor)
    #         x, y = neighbor[0], neighbor[1]
    #
    #         if x < 0 or x > (WIDTH - SQUARE_SIZE):
    #             neighbors.remove(neighbor)
    #             print(f"X out of bounds: {x}")
    #         # We know that the coordinates are valid; now we check if the type is
    #         if y < 0 or y > (HEIGHT - SQUARE_SIZE):
    #             neighbors.remove(neighbor)
    #             print(f"Y out of bounds: {y}")
    #         # else:
    #         #     neighbor_square = self.__squares[(x, y)]
    #         #     if neighbor_square.square_type is not SquareType.WALL:
    #         #         neighbors.remove(neighbor)
    #
    #     for neighbor in neighbors:
    #         neighbor_square = self.__squares[neighbor]
    #         if neighbor_square.square_type is not SquareType.WALL:
    #             neighbors.remove(neighbor)
    #
    #     # print(neighbors)
    #     # Out of the remaining valid neighbors, randomly select and return one
    #     random_index = random.randrange(0, len(neighbors))
    #     coordinates = neighbors[random_index]
    #     # print(coordinates)
    #     return self.__squares[coordinates]
    #
    # # Using randomized DFS to generate a maze
    # def generate_maze(self):
    #     # Initialize all squares to walls
    #     for square in self.__squares.values():
    #         square.square_type = SquareType.WALL
    #
    #     stack = []
    #
    #     # Pick a random node to make normal
    #     rand_x, rand_y = random.randrange(0, WIDTH - SQUARE_SIZE, SQUARE_SIZE), random.randrange(0,
    #                                                                                              HEIGHT - SQUARE_SIZE,
    #                                                                                              SQUARE_SIZE)
    #
    #     rand_square = self.__squares[(rand_x, rand_y)]
    #     rand_square.square_type = SquareType.NORMAL
    #
    #     # Append the first chosen node into the stack
    #     stack.append(rand_square)
    #
    #     iteration = 0
    #
    #     while stack:
    #         iteration += 1
    #         # print(iteration)
    #
    #         # Pop a node from the stack
    #         current = stack.pop()
    #         # print(current)
    #
    #         # Now we need to get an unvisited neighbor (if there are any)
    #         chosen_neighbor = self.__get_maze_neighbor(current)
    #
    #         if chosen_neighbor:
    #             # while 0 <= neighbors[direction_choice].x < WIDTH and 0 <= neighbors[direction_choice].y < HEIGHT \
    #             #         and neighbors[direction_choice].square_type is not SquareType.WALL:
    #             #     direction_choice = random.randrange(0, 4)
    #
    #             # print(chosen_neighbor)
    #             chosen_neighbor.square_type = SquareType.NORMAL
    #
    #             # find the midpoint between the current square and chosen neighbor
    #             midpoint = ((current.x + chosen_neighbor.x) // 2, (current.y + chosen_neighbor.y) // 2)
    #             midpoint_square = self.__squares[midpoint]
    #             midpoint_square.square_type = SquareType.NORMAL
    #
    #             self.__event_manager.post(TickEvent())
    #
    #             stack.append(chosen_neighbor)

    def dijkstra(self, render):
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
                    # new_tick = TickEvent((self.__squares, pq))
                    # self.__event_manager.post(new_tick)

                if v == self.__end or v.square_type is SquareType.END:
                    # TODO: Notify all listeners that the algorithm has terminated and post the shortest path in the
                    #  event
                    self.shortest_path = self.get_shortest_path()
                    # print(self.shortest_path)
                    # self.__event_manager.post(StateChangeEvent(StateType.ENDED))
                    return v

    def get_shortest_path(self):
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


class GraphicalView(object):
    # TODO: Create a new method here that creates a new square based on click position
    # Drawing will instead be handled on a square to square level rather than iterating the entire squares list
    # Lambda functions will be used for this purpose to allow drawing to occur
    """
    Draws the model state onto the screen.
    """

    def __init__(self, model):
        """
        event_manager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.

        Attributes:
        is_initialized (bool): pygame is ready to draw.
        screen (pygame.Surface): the screen surface.
        clock (pygame.time.Clock): keeps the fps constant.
        small_font (pygame.Font): a small font.
        """

        self.model = model
        self.running = False
        self.screen = None
        self.clock = None
        self.small_font = None

    def render_all(self):
        for square in self.model.squares.values():
            if square.square_type is SquareType.NORMAL:
                pygame.draw.rect(self.screen, GRAY, (square.x, square.y, SQUARE_SIZE, SQUARE_SIZE), 3)
            elif square.square_type is SquareType.START:
                pygame.draw.rect(self.screen, GREEN, (square.x, square.y, SQUARE_SIZE, SQUARE_SIZE))
            elif square.square_type is SquareType.END:
                pygame.draw.rect(self.screen, RED, (square.x, square.y, SQUARE_SIZE, SQUARE_SIZE))
            elif square.square_type is SquareType.DONE:
                pygame.draw.rect(self.screen, ORANGE, (square.x, square.y, SQUARE_SIZE, SQUARE_SIZE), 3)
            elif square.square_type is SquareType.WALL:
                pygame.draw.rect(self.screen, BLACK, (square.x, square.y, SQUARE_SIZE, SQUARE_SIZE))

        pygame.display.flip()

    def render_path(self):
        for square in self.model.shortest_path:
            pygame.draw.rect(self.screen, ORANGE, (square.x, square.y, SQUARE_SIZE, SQUARE_SIZE))

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('demo game')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.small_font = pygame.font.Font(None, 40)
        self.screen.fill(WHITE)
        self.render_all()

    def run(self):
        self.initialize()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    x, y = click_pos[0], click_pos[1]

                    # The user has left clicked
                    if event.button == 1:
                        # Check if the start has been set
                        if not self.model.start:
                            self.model.handle_click(click_pos, ClickOperation.SET_START, lambda: self.render_all())
                        elif not self.model.end:
                            self.model.handle_click(click_pos, ClickOperation.SET_END, lambda: self.render_all())
                        else:
                            self.model.handle_click(click_pos, ClickOperation.SET_WALL, lambda: self.render_all())
                    # The user has right clicked
                    # elif event.button == 3:
                    #     self.model.handle_click(click_pos)

            # if current_state == model.StateType.SELECTION:
            #     self.render_all()
            # if current_state == model.StateType.RUNNING:
            #     self.render_all()
            # if current_state == model.StateType.PAUSED:
            #     self.render_all()
            # if current_state == model.StateType.ENDED:
            #     # First draw the grid and then draw the shortest path
            #     self.render_all()
            #     self.render_path()

            self.clock.tick(60)

        pygame.quit()

    # def handle_click(self, click_pos, click_state, draw):
    #     x, y = click_pos[0], click_pos[1]
    #
    #     for square in self.__squares.values():
    #         if square.coordinate_in_square(x, y):
    #             if click_state is ClickOperation.SET_START:
    #                 square.square_type = SquareType.START
    #                 self.__start = square
    #                 draw()
    #             elif click_state is ClickOperation.SET_END:
    #                 square.square_type = SquareType.END
    #                 self.__end = square
    #                 draw()
    #             elif click_state is ClickOperation.SET_WALL:
    #                 square.square_type = SquareType.WALL
    #                 draw()

if __name__ == "__main__":
    m = Model()
    v = GraphicalView(m)
    v.run()
