"""
Module level details

...

Classes
-------
    Model
    GraphicalView
    SquareType(Enum)
    ClickOperation(Enum

Functions
---------
    get_clicked_pos(pos, rows, width) -> (int, int)

Notes
-----
Uses pygame and heapdict (priority queue/heap implementation)
"""

import pygame
from heapdict import heapdict
import math
from enum import Enum, IntEnum

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
unreachable_e = pygame.event.Event(pygame.USEREVENT, attr='unreachable')


class GameState(Enum):
    SELECTION = 0,
    RUNNING = 1,
    DONE = 2,
    ERROR = 3


class AlgorithmType(IntEnum):
    DIJKSTRA = 0,
    A_STAR = 1


class SquareType(Enum):
    START = 0,
    END = 1,
    WALL = 2,
    NORMAL = 3,
    DONE = 4


class Square:
    """
    This class encapsulates all inner state of the visualizer.
    This includes, application logic and the grid with all of its respective squares.

    ...

    Attributes
    ----------
    __x : int
        x position of square in grid (each grid square corresponds to one (x, y) position
    __y : int
        y position of square in grid (each grid square corresponds to one (x, y) position
    __prev : Square
        The previous neighbor of a square; only relevant for Dijkstra's Algorithm
    __u_x : int
        A translated version of x position; this is used for drawing purposes only
    __u_y : int
        A translated version of y position; this is used for drawing purposes only
    __distance_from_source : int
        Indicates the distance of the square from the source node (start). Used for Dijkstra's.
    __neighbors : list[Square]
        The neighbors of the square. Used for Dijkstra's.
    square_type : SquareType
        An enum value of the particular square type (used for distinguishing squares in Dijkstra's).

    Methods
    -------
    render_square(window):
        Renders the current square
    collides(other):
        Essentially __eq__ implementation; checks if current square and other square are equal.
    """

    def __init__(self, x, y, prev=None, distance_from_source=float("inf"), square_type=SquareType.NORMAL):
        self.__x = x
        self.__y = y
        self.__u_x = x * SQUARE_SIZE
        self.__u_y = y * SQUARE_SIZE
        self.__distance_from_source = distance_from_source
        self.__neighbors = []
        self.__square_type = square_type
        self.__prev = prev

    # Beginning of getters/setters
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

    @property
    def u_x(self):
        return self.__u_x

    @u_x.setter
    def u_x(self, value):
        self.__u_x = value

    # End of getters/setters

    def render_square(self, window):
        """
        A method for drawing a square.

        Parameters
        ----------
        window : pygame.Surface
            The screen object for drawing
        """
        if self.square_type is SquareType.NORMAL:
            pygame.draw.rect(window, GRAY, (self.__u_x, self.__u_y, SQUARE_SIZE, SQUARE_SIZE), 3)
        if self.square_type is SquareType.START:
            pygame.draw.rect(window, GREEN, (self.__u_x, self.__u_y, SQUARE_SIZE, SQUARE_SIZE))
        if self.square_type is SquareType.END:
            pygame.draw.rect(window, RED, (self.__u_x, self.__u_y, SQUARE_SIZE, SQUARE_SIZE))
        if self.square_type is SquareType.DONE:
            pygame.draw.rect(window, ORANGE, (self.__u_x, self.__u_y, SQUARE_SIZE, SQUARE_SIZE), 3)
        if self.square_type is SquareType.WALL:
            pygame.draw.rect(window, BLACK, (self.__u_x, self.__u_y, SQUARE_SIZE, SQUARE_SIZE))

    def __str__(self):
        return f"Square at position: ({self.x}, {self.y}) of type: {self.__square_type}"

    def collides(self, other):
        """
        Determines whether or not the current square matches another given square.

        Parameters
        ----------
        other : Square
            The other square to check for equality
        Returns
        -------
        bool
            Whether or not the input square is equal to this square

        Notes
        -----
        The decision to implement this functionality in a custom method instead of __eq__ was to ensure that heapdict
        works properly (as overriding __eq__ alters the default hashing implementation).
        """
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
    """
        This class encapsulates all inner state of the visualizer.
        This includes application logic and the grid with all of its respective squares.

        ...

        Attributes
        ----------
        __squares : dict of form (int, int) : Square
            x position of square in grid (each grid square corresponds to one (x, y) position
        __start : Square
            The start square as a source for Dijkstra's algorithm
        __end : Square
            The end square as a destination for Dijkstra's algorithm
        __running : bool
            Whether or not pygame loop is running
        shortest_path : list of Square(s)
            Represents the shortest path from start to end
        game_state : GameState enum
            Represents the current state of the game
        algorithm_type : AlgorithmType enum
            Represents the currently chosen graph pathfinding algorithm


        Methods
        -------
        reset_grid():
            Resets every square in the grid to its default state
        get_neighbors(square):
            Gets neighbors of a given square
        dijkstra(draw):
            Dijkstra's algorithm implementation based on Euclidean distance
        __h(a, b):
            Private heuristic method that acts as a subroutine for the A* algorithm
        a_star(draw):
            A* algorithm implementation based on Manhattan distance
        get_shortest_path():
            Returns the shortest path
        cycle_algorithm():
            Based on user input, changes the current algorithm through cycling available options
        """

    def __init__(self):
        self.__squares = {(x, y): Square(x, y) for x in range(0, (WIDTH // SQUARE_SIZE)) for y in
                          range(0, (HEIGHT // SQUARE_SIZE))}
        self.__start = None
        self.__end = None
        self.__running = False
        self.shortest_path = []
        self.game_state = GameState.SELECTION
        self.algorithm_type = AlgorithmType.DIJKSTRA

    def reset_grid(self):
        """
        Resets the grid of squares to default state
        """
        self.__squares = {(x, y): Square(x, y) for x in range(0, (WIDTH // SQUARE_SIZE)) for y in
                          range(0, (HEIGHT // SQUARE_SIZE))}

    def get_neighbors(self, square):
        """

        Parameters
        ----------
        square : Square
            The square for which neighbors are found

        Returns
        -------
        square.neighbors : list of Square(s)
            Returns the neighbors of the square

        Notes
        -----
        Essentially sets the list of neighbors and then returns it. Neighbors are squares at any distance of 1 away
        from this square.

        """
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

    def dijkstra(self, draw, clock):
        r"""
        An implementation of Dijkstra's algorithm for squares on a grid.

        Parameters
        ----------
        draw : void lambda function
            Draws all of the squares. Passed in from GraphicalView

        Returns
        -------
        v : Square
            The end square once it has been reached by the algorithm.

        Notes
        -----
        This particular implementation of Dijkstra's algorithm makes use of a heapdict, which is essentially
        a priority queue. This ensures :math: `O((|V| + |E|)\log|V|)` time complexity. Implementation is similar to a
        traditional adjacency list implementation of Dijkstra's algorithm, in that the operation to find neighbors
        runs in :math: `O(1)` time. As each square is reached, its state is changed to SquareType.DONE. If the end
        square is reached, the shortest path is determined and the algorithm terminates by returning the end node.
        If the end node isn't reached, i.e. no path exists from start to end, then the while loop exits as the pq is
        empty. A event is therefore posted to display an error message.
        """
        i = 0
        pq = heapdict()
        # The start square's distance from itself is 0
        pq[self.__start] = 0

        while pq:
            # A tuple is returned, where the fist item is the square and the second value is distance (priority)
            u = pq.popitem()[0]

            neighbors = self.get_neighbors(u)
            for v in neighbors:

                if v.square_type is SquareType.NORMAL or v.square_type is SquareType.END:
                    cost = math.dist((u.x, u.y), (v.x, v.y))

                    if u.distance_from_source + cost < v.distance_from_source:
                        v.distance_from_source = u.distance_from_source + cost
                        v.prev = u

                        # Only change type to DONE if the square is not the end square
                        if v.square_type is not SquareType.END:
                            v.square_type = SquareType.DONE

                        # Decrease priority (update the priority of current square in priority queue)
                        pq[v] = v.distance_from_source

                # TODO: Tick update here: one iteration of the algorithm has finished, we now need to update.
                # Unsure how to implement this correctly...

                # Instead of posting a tick event to the pygame event queue, draw() is directly called here
                # TODO: drawing at each algorithm step is required, but it appears to cause significant lag;
                #  how can this lag be fixed? Unsure if it is due to dijkstra being called in pygame event queue loop.
                # draw()

                if i % 30 == 0:
                    draw()

                i += 1

                # The end square has been reached
                if v == self.__end or v.square_type is SquareType.END:
                    self.shortest_path = self.get_shortest_path()
                    # Notify the pygame event queue that the algorithm has terminated: draw the shortest path
                    pygame.event.post(done_e)

                    return v
            # clock.tick(60)

        # print("Algorithm terminated and pq empty")
        pygame.event.post(unreachable_e)

    def __h(self, a, b):
        """
        Heuristic method that is used as a subroutine in A*

        Parameters
        ----------
        a : Square
            The current square
        b : Square
            Another square for which the  Manhattan distance is found

        Returns
        -------
        int
            The Manhattan distance between a and b.
        """
        return abs(a.x - b.x) + abs(a.y - b.y)

    def a_star(self, draw):
        """
        Implementation of the A* pathfinding algorithm using Manhattan distance as a heuristic function.

        Parameters
        ----------
        draw : void lambda method

        Returns
        -------
        v : Square
            The end node once it is reached

        Notes
        -----

        """
        i = 0
        pq = heapdict()
        # The start square's distance from itself is 0
        pq[self.__start] = 0

        while pq:
            # A tuple is returned, where the fist item is the square and the second value is distance (priority)
            u = pq.popitem()[0]

            neighbors = self.get_neighbors(u)
            for v in neighbors:

                if v.square_type is SquareType.NORMAL or v.square_type is SquareType.END:
                    cost = math.dist((u.x, u.y), (v.x, v.y))

                    if u.distance_from_source + cost < v.distance_from_source:
                        v.distance_from_source = u.distance_from_source + cost
                        v.prev = u

                        # Only change type to DONE if the square is not the end square
                        if v.square_type is not SquareType.END:
                            v.square_type = SquareType.DONE

                        # Decrease priority (update the priority of current square in priority queue)
                        # Update priority based on the heuristic method
                        pq[v] = v.distance_from_source + self.__h(self.end, v)

                if i % 30 == 0:
                    draw()

                i += 1

                # The end square has been reached
                if v == self.__end or v.square_type is SquareType.END:
                    self.shortest_path = self.get_shortest_path()
                    # Notify the pygame event queue that the algorithm has terminated: draw the shortest path
                    pygame.event.post(done_e)

                    return v
            # clock.tick(60)

        # print("Algorithm terminated and pq empty")
        pygame.event.post(unreachable_e)

    def get_shortest_path(self):
        """
        Get the shortest path from start to end

        Returns
        -------
        path : List of Square(s)
            Represents the shortest path chain of Square objects from start to end
        """
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

    def cycle_algorithm(self):
        i = int(self.algorithm_type)
        self.algorithm_type = (i + 1) % len(AlgorithmType)
        print(self.algorithm_type)


def get_clicked_pos(pos, rows, width):
    """
    Returns the coordinates of the particular square the user has clicked.

    Parameters
    ----------
    pos : (int, int)
        Tuple of integers representing (x, y) clicked position
    rows : int
        The number of rows. Calculated by dividing WIDTH by SQUARE_SIZE
    width : int
        The width of the screen. As width = height in this program, this can also be considered height.

    Returns
    -------
    (row, col) : (int, int)
        A tuple of integers representing the clicked square's position

    Notes
    -----
    Please note that there are two separate (x, y) coordinates for each square: (u_x, u_y)–used for drawing
    purposes–that represents the true (x, y) coordinate of each square as they appear on the screen (analogous to
    pygame's square.left and square.top points); as well as (x, y), which represents the position of a given square for
    access in the squares dictionary.

    0 ≤ x ≤ WIDTH // SQUARE_SIZE and 0 ≤ y ≤ HEIGHT // SQUARE_SIZE
    """
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


# Class structure adapted from MVC-game-design as found in references section
class GraphicalView:
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

    # def render_all(self):
    #     for square in self.model.squares.values():
    #         if square.square_type is SquareType.NORMAL:
    #             pygame.draw.rect(self.screen, GRAY, (square.u_x, square.u_y, SQUARE_SIZE, SQUARE_SIZE), 3)
    #         elif square.square_type is SquareType.START:
    #             pygame.draw.rect(self.screen, GREEN, (square.u_x, square.u_y, SQUARE_SIZE, SQUARE_SIZE))
    #         elif square.square_type is SquareType.END:
    #             pygame.draw.rect(self.screen, RED, (square.u_x, square.u_y, SQUARE_SIZE, SQUARE_SIZE))
    #         elif square.square_type is SquareType.DONE:
    #             pygame.draw.rect(self.screen, ORANGE, (square.u_x, square.u_y, SQUARE_SIZE, SQUARE_SIZE), 3)
    #         elif square.square_type is SquareType.WALL:
    #             pygame.draw.rect(self.screen, BLACK, (square.u_x, square.u_y, SQUARE_SIZE, SQUARE_SIZE))
    #
    #     pygame.display.update()

    def draw(self):
        """
        Iterate over each square in squares and call its respective draw method
        """
        for square in self.model.squares.values():
            square.render_square(self.screen)

        pygame.display.update()

    def render_path(self):
        """
        Draw the shortest path from start to end.
        """
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
        """
        The pygame main loop. Consists of the game loop and pygame event queue loop. Handles mouse click events, key
        pressed events, as well as certain user-created events.

        Notes
        -----
        Certain implementation is not yet present (such as erasing squares). In addition, error handling isn't yet
        implemented.
        """
        self.initialize()
        self.running = True

        while self.running:
            for event in pygame.event.get():
                # Only consider using tick events if the algorithm can redraw at each increment without lag
                # if event == tick_e:
                #     self.draw()
                # The algorithm has terminated; draw the shortest path
                if event == done_e:
                    self.render_path()
                    self.model.game_state = GameState.DONE
                if event == unreachable_e:
                    print("The end square was blocked; no path could be found!")

                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    # Space key for start/stopping the visualizer
                    # As of now, only starting the visualizer works
                    if self.model.game_state is GameState.RUNNING:
                        if event.key == pygame.K_SPACE and self.model.start and self.model.end:
                            if self.model.algorithm_type is AlgorithmType.DIJKSTRA:
                                self.model.dijkstra(lambda: self.draw(), self.clock)
                            else:
                                self.model.a_star(lambda: self.draw())

                    # Clearing the entire grid
                    elif event.key == pygame.K_c:
                        self.model.start = None
                        self.model.end = None
                        self.model.reset_grid()
                        self.screen.fill(WHITE)
                        self.draw()

                    elif event.key == pygame.K_a:
                        print("Change algorithm")
                        self.model.cycle_algorithm()

                # The user has left clicked
                if pygame.mouse.get_pressed()[0]:
                    if self.model.game_state is GameState.SELECTION:
                        click_pos = pygame.mouse.get_pos()

                        # Get the (x, y) position of the clicked square
                        row, col = (get_clicked_pos(click_pos, (WIDTH // SQUARE_SIZE), WIDTH))

                        # Check if the start has been set
                        if not self.model.start:
                            square = Square(row, col, None, 0, SquareType.START)

                            self.model.start = square
                            self.model.squares[(row, col)] = square

                        # Only allow the end square to be set if the start square has been set
                        elif not self.model.end and self.model.start:
                            square = Square(row, col, None, float("inf"), SquareType.END)

                            # Don't allow the end square to be added unless it is a different square from the start
                            # square
                            if not square.collides(self.model.start):
                                self.model.end = square
                                self.model.squares[(row, col)] = square
                                self.model.game_state = GameState.RUNNING

                        # Only allow creation of walls if the start and end squares have been set
                        elif self.model.start and self.model.end:
                            square = Square(row, col, None, 0, SquareType.WALL)

                            # Ensure that the clicked position for a wall isn't that of the start or end square
                            if not square.collides(self.model.start) and not square.collides(self.model.end):
                                self.model.squares[(row, col)] = square

                    # The user has right clicked
                    # Deletion of independent squares
                    elif pygame.mouse.get_pressed()[2]:
                        click_pos = pygame.mouse.get_pos()
                        row, col = (get_clicked_pos(click_pos, (WIDTH // SQUARE_SIZE), WIDTH))

                        square = self.model.squares[(row, col)]

                        if square == self.model.start:
                            self.model.start = None
                            self.model.squares[(row, col)] = Square(row, col, None, float("inf"), SquareType.NORMAL)
                            pygame.draw.rect(self.screen, WHITE,
                                             (square.x * SQUARE_SIZE, square.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                            self.draw()

                        elif square == self.model.end:
                            self.model.end = None
                            self.model.squares[(row, col)] = Square(row, col, None, float("inf"), SquareType.NORMAL)
                            pygame.draw.rect(self.screen, WHITE,
                                             (square.x * SQUARE_SIZE, square.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                            self.draw()

                        elif square.square_type is SquareType.WALL:
                            self.model.squares[(row, col)] = Square(row, col, None, float("inf"), SquareType.NORMAL)
                            pygame.draw.rect(self.screen, WHITE,
                                             (square.x * SQUARE_SIZE, square.y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                            self.draw()
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    m = Model()
    v = GraphicalView(m)
    v.run()
