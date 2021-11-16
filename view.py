import pygame
import model
from eventmanager import *

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255,165,0)


class GraphicalView(object):
    """
    Draws the model state onto the screen.
    """

    def __init__(self, event_manager, model):
        """
        event_manager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.

        Attributes:
        is_initialized (bool): pygame is ready to draw.
        screen (pygame.Surface): the screen surface.
        clock (pygame.time.Clock): keeps the fps constant.
        small_font (pygame.Font): a small font.
        """

        self.__event_manager = event_manager
        self.__event_manager.register_listener(self)
        self.model = model
        self.is_initialized = False
        self.screen = None
        self.clock = None
        self.small_font = None

    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """

        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.is_initialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            if not self.is_initialized:
                return
            # Get the current state
            current_state = self.model.state.peek()

            if current_state == model.StateType.SELECTION:
                self.render_all()
            if current_state == model.StateType.RUNNING:
                self.render_all()
            if current_state == model.StateType.PAUSED:
                self.render_all()
            if current_state == model.StateType.ENDED:
                # First draw the grid and then draw the shortest path
                self.render_all()
                self.render_path()

            # limit the redraw speed to 30 frames per second
            self.clock.tick(60)

    # def render_selection(self):
    #     """
    #     Render the game menu.
    #     """
    #
    #     self.screen.fill((0, 0, 0))
    #     some_words = self.small_font.render(
    #         'You are in the selection screen. Space to play. Esc exits.',
    #         True, (0, 255, 0))
    #     self.screen.blit(some_words, (0, 0))
    #     pygame.display.flip()

    def render_run(self):
        """
        Render the game play.
        """

        self.screen.fill((0, 0, 0))
        some_words = self.small_font.render(
            'You are Playing the game. F1 for help.',
            True, (0, 255, 0))
        self.screen.blit(some_words, (0, 0))
        pygame.display.flip()

    def render_pause(self):
        """
        Render the help screen.
        """

        self.screen.fill((0, 0, 0))
        some_words = self.small_font.render(
            'You have paused. space, escape or return.',
            True, (0, 255, 0))
        self.screen.blit(some_words, (0, 0))
        pygame.display.flip()

    # def init_grid(self):
    #     for x in range(0, model.WIDTH, 20):
    #         for y in range(0, model.HEIGHT, 20):
    #             pygame.draw.rect(self.screen, GRAY, (x, y, model.SQUARE_SIZE, model.SQUARE_SIZE), 3)

    # Only one draw method is needed
    # This draw method draws all of the squares on the screen
    # Potentially in the future when running dijkstra a second draw method and/or events may be required
    def render_all(self, event=None):
        # self.init_grid()

        for square in self.model.squares.values():
            if square.square_type is model.SquareType.NORMAL:
                pygame.draw.rect(self.screen, GRAY, (square.x, square.y, model.SQUARE_SIZE, model.SQUARE_SIZE), 3)
            elif square.square_type is model.SquareType.START:
                pygame.draw.rect(self.screen, GREEN, (square.x, square.y, model.SQUARE_SIZE, model.SQUARE_SIZE))
            elif square.square_type is model.SquareType.END:
                pygame.draw.rect(self.screen, RED, (square.x, square.y, model.SQUARE_SIZE, model.SQUARE_SIZE))
            elif square.square_type is model.SquareType.DONE:
                pygame.draw.rect(self.screen, ORANGE, (square.x, square.y, model.SQUARE_SIZE, model.SQUARE_SIZE), 3)

        pygame.display.flip()

    def render_path(self):
        for square in self.model.shortest_path:
            pygame.draw.rect(self.screen, ORANGE, (square.x, square.y, model.SQUARE_SIZE, model.SQUARE_SIZE))

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        # result = pygame.init()
        pygame.font.init()
        pygame.display.set_caption('demo game')
        self.screen = pygame.display.set_mode((model.WIDTH, model.HEIGHT))
        self.clock = pygame.time.Clock()
        self.small_font = pygame.font.Font(None, 40)
        self.is_initialized = True
        self.screen.fill(WHITE)
        self.render_all()
