"""
Classes:
    Model
    GraphicalView
    SquareType(Enum)
    ClickOperation(Enum

Functions:
    get_clicked_pos(pos, rows, width) -> int tuple
    
Uses pygame and heapdict (priority queue/heap implementation)
"""
import pygame
from heapdict import heapdict
import math
from enum import Enum

# Constants
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
WIDTH = HEIGHT = 600
SQUARE_SIZE = 20

# User events
tick_e = pygame.event.Event(pygame.USEREVENT, attr1='tick')
done_e = pygame.event.Event(pygame.USEREVENT, attr1='done')


class SquareType(Enum):
    START = 1,
    END = 2,
    WALL = 3,
    NORMAL = 4,
    DONE = 5


class Square:
    """
    This class encapsulates all inner state of the visualizer.
    This includes, application logic and the grid with all of its respective squares.

    ...

    Attributes
    ----------
    x : int
        x position of square
    y : int
        y position of square
    prev : int

    """
    def __init__(self, x, y, prev=None, distance_from_source=float("inf"), square_type=SquareType.NORMAL):
        self.__x = x
        self.__y = y
        self.u_x = x * SQUARE_SIZE
        self.u_y = y * SQUARE_SIZE
        self.__distance_from_source = distance_from_source
        self.__neighbors = []
        self.__square_type = square_type
        self.__prev = prev

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
    def prev(self):
        return self.__prev

    @prev.setter
    def prev(self, value):
        self.__prev = value

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

    def render_square(self, window):
        x, y = self.x * SQUARE_SIZE, self.y * SQUARE_SIZE
        if self.square_type is SquareType.NORMAL:
            pygame.draw.rect(window, GRAY, (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)
        if self.square_type is SquareType.START:
            pygame.draw.rect(window, GREEN, (x, y, SQUARE_SIZE, SQUARE_SIZE))
        if self.square_type is SquareType.END:
            pygame.draw.rect(window, RED, (x, y, SQUARE_SIZE, SQUARE_SIZE))
        if self.square_type is SquareType.DONE:
            pygame.draw.rect(window, ORANGE, (x, y, SQUARE_SIZE, SQUARE_SIZE), 3)
        if self.square_type is SquareType.WALL:
            pygame.draw.rect(window, BLACK, (x, y, SQUARE_SIZE, SQUARE_SIZE))

    def __str__(self):
        return f"Square at position: ({self.x}, {self.y}) of type: {self.__square_type}"

    def collides(self, other):
        return self.__x == other.x and self.y == other.y

    # def __eq__(self, other):
    #     return self.x == other.x and self.y == other.y
    #
    # def __hash__(self):
    #     return hash((self.__x, self.__y))
    #
    # def __lt__(self, other):
    #     return (self.__x, self.__y) < (other.x, other.y)


class Model:
    def __init__(self):
        # All of type Square When we first initialize the model, we want to set the initial state of all of the
        # squares. We want to create a square for each position in the grid
        self.__squares = {(x, y): Square(x, y) for x in range(0, (WIDTH // SQUARE_SIZE)) for y in
                          range(0, (HEIGHT // SQUARE_SIZE))}
        # self.__squares = {}
        self.__start = None
        self.__end = None
        self.__running = False
        self.shortest_path = []

    def reset_grid(self):
        self.__squares = {(x, y): Square(x, y) for x in range(0, (WIDTH // SQUARE_SIZE)) for y in
                          range(0, (HEIGHT // SQUARE_SIZE))}

    def get_neighbors(self, square):
        if square.y - 1 >= 0:
            neighbor = self.__squares[(square.x, square.y - 1)]
            square.neighbors.append(neighbor)
        if square.x - 1 >= 0:
            neighbor = self.__squares[(square.x - 1, square.y)]
            square.neighbors.append(neighbor)
        if square.x + 1 < (WIDTH // SQUARE_SIZE):
            neighbor = self.__squares[(square.x + 1, square.y)]
            square.neighbors.append(neighbor)
        if square.y + 1 < (HEIGHT // SQUARE_SIZE):
            neighbor = self.__squares[(square.x, square.y + 1)]
            square.neighbors.append(neighbor)

        return square.neighbors

    def dijkstra(self, draw):
        pq = heapdict()
        pq[self.__start] = 0

        while pq:
            # A tuple is returned, where the fist item is the priority and the second value is square
            u = pq.popitem()[0]
            # print(f"u: {u}")

            neighbors = self.get_neighbors(u)
            for v in neighbors:
                # print(f"v: {v}")

                if v.square_type is SquareType.NORMAL or v.square_type is SquareType.END:
                    cost = math.dist((u.x, u.y), (v.x, v.y))

                    if u.distance_from_source + cost < v.distance_from_source:
                        v.distance_from_source = u.distance_from_source + cost
                        v.prev = u

                        if v.square_type is not SquareType.END:
                            # print(v)
                            v.square_type = SquareType.DONE

                        pq[v] = v.distance_from_source

                    # TODO: Tick update here: one iteration of the algorithm has finished, we now need to update
                    # We want to encapsulate the entire grid and priority queue to be able to draw the updated state
                    # new_tick = TickEvent((self.__squares, pq))
                    # self.__event_manager.post(new_tick)
                    # v.render_square(screen)
                    pygame.event.post(tick_e)

                # clock.tick(60)
                draw()

                if v == self.__end or v.square_type is SquareType.END:
                    # TODO: Notify all listeners that the algorithm has terminated and post the shortest path in the
                    #  event
                    self.shortest_path = self.get_shortest_path()
                    # print(v)
                    print("Finished")
                    print(self.shortest_path)
                    # self.__event_manager.post(StateChangeEvent(StateType.ENDED))
                    # v.render_square(screen)
                    pygame.event.post(done_e)

                    return v

    def get_shortest_path(self):
        current_square = self.__end
        path = []

        while current_square.prev:
            path.append(current_square)
            current_square = current_square.prev

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


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


class GraphicalView:
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
                pygame.draw.rect(self.screen, GRAY, (square.u_x, square.u_y, SQUARE_SIZE, SQUARE_SIZE), 3)
            elif square.square_type is SquareType.START:
                pygame.draw.rect(self.screen, GREEN, (square.u_x, square.u_y, SQUARE_SIZE, SQUARE_SIZE))
            elif square.square_type is SquareType.END:
                pygame.draw.rect(self.screen, RED, (square.u_x, square.u_y, SQUARE_SIZE, SQUARE_SIZE))
            elif square.square_type is SquareType.DONE:
                pygame.draw.rect(self.screen, ORANGE, (square.u_x, square.u_y, SQUARE_SIZE, SQUARE_SIZE), 3)
            elif square.square_type is SquareType.WALL:
                pygame.draw.rect(self.screen, BLACK, (square.u_x, square.u_y, SQUARE_SIZE, SQUARE_SIZE))

        pygame.display.update()

    def draw(self):
        for square in self.model.squares.values():
            square.render_square(self.screen)

        pygame.display.update()

    def render_path(self):
        for square in self.model.shortest_path:
            pygame.draw.rect(self.screen, ORANGE,
                             (square.x * SQUARE_SIZE, square.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

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
        self.draw()

    def run(self):
        self.initialize()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event == tick_e:
                    pass
                if event == done_e:
                    # for square in self.model.squares.values():
                    #     if square.square_type is SquareType.DONE:
                    #         # print(square)
                    self.render_path()

                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    # Space key for start/stopping the visualizer
                    if event.key == pygame.K_SPACE and self.model.start and self.model.end:
                        self.model.dijkstra(lambda: self.draw())

                    elif event.key == pygame.K_c:
                        self.model.start = None
                        self.model.end = None
                        self.model.reset_grid()
                        self.draw()

                # The user has left clicked
                if pygame.mouse.get_pressed()[0]:
                    click_pos = pygame.mouse.get_pos()

                    row, col = (get_clicked_pos(click_pos, (WIDTH // SQUARE_SIZE), WIDTH))
                    # Check if the start has been set
                    if not self.model.start:
                        square = Square(row, col, -1, 0, SquareType.START)

                        self.model.start = square
                        self.model.squares[(row, col)] = square

                    elif not self.model.end and self.model.start:
                        square = Square(row, col, -1, float("inf"), SquareType.END)

                        if not square.collides(self.model.start):
                            print(square)
                            self.model.end = square
                            self.model.squares[(row, col)] = square

                    elif self.model.start and self.model.end:
                        square = Square(row, col, -1, 0, SquareType.WALL)

                        if not square.collides(self.model.start) and not square.collides(self.model.end):
                            self.model.squares[(row, col)] = square

                    # The user has right clicked
                elif pygame.mouse.get_pressed()[2]:
                    click_pos = pygame.mouse.get_pos()
                    row, col = (get_clicked_pos(click_pos, (WIDTH // SQUARE_SIZE), WIDTH))

                    square = self.model.squares[(row, col)]

                    if square == self.model.start:
                        self.model.start = None
                        self.model.squares[(row, col)] = Square(row, col, -1, float("inf"), SquareType.NORMAL)
                        print(self.model.start)
                        print(self.model.squares[(row, col)])

                    elif square == self.model.end:
                        print("Erase end")

            self.draw()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    m = Model()
    v = GraphicalView(m)
    v.run()
