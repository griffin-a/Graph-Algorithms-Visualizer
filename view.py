import pygame
import model
from eventmanager import *

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


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
                self.render_grid(event)
            if current_state == model.StateType.RUNNING:
                self.render_grid()
            if current_state == model.StateType.PAUSED:
                self.render_pause()

            # limit the redraw speed to 30 frames per second
            self.clock.tick(30)

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

    # Draw each of the squares on the screen
    # In reality, this is the only draw method that we need
    def render_grid(self, event=None):

        # self.screen.fill(WHITE)

        # The number of squares is: (WIDTH / square width/height) * (HEIGHT / square width/height)
        # Use this information to generate each of the squares
        # for x in range(0, model.WIDTH, 20):
        #     for y in range(0, model.HEIGHT, 20):
        #         pygame.draw.rect(self.screen, GRAY, (x, y, model.SQUARE_SIZE, model.SQUARE_SIZE), 3)

        if event.state:
            squares = event.state
            print(len(squares))

            for square in squares:
                if square.square_type is model.SquareType.NORMAL:
                    pygame.draw.rect(self.screen, GRAY, (square.x, square.y, model.SQUARE_SIZE, model.SQUARE_SIZE), 3)
                elif square.square_type is model.SquareType.START:
                    pygame.draw.rect(self.screen, GREEN, (square.x, square.y, model.SQUARE_SIZE, model.SQUARE_SIZE))
                elif square.square_type is model.SquareType.END:
                    pygame.draw.rect(self.screen, RED, (square.x, square.y, model.SQUARE_SIZE, model.SQUARE_SIZE))
        # if event.state:
        #     state = event.state
        #     # Tick events will either be one square (start/end) or all of the squares on the grid
        #     if event.name == "start":
        #         pygame.draw.rect(self.screen, GREEN, (state.x, state.y, model.SQUARE_SIZE, model.SQUARE_SIZE))
        #     elif event.name == "end":
        #         print("End needs to be drawn")
        #         pygame.draw.rect(self.screen, RED, (state.x, state.y, model.SQUARE_SIZE, model.SQUARE_SIZE))
        pygame.display.flip()

    def init_grid(self):
        for x in range(0, model.WIDTH, 20):
            for y in range(0, model.HEIGHT, 20):
                pygame.draw.rect(self.screen, GRAY, (x, y, model.SQUARE_SIZE, model.SQUARE_SIZE), 3)

    def render_selection(self, event=None):
        if event.state:
            state = event.state
            # Tick events will either be one square (start/end) or all of the squares on the grid
            if event.name == "start":
                pygame.draw.rect(self.screen, GREEN, (state.x, state.y, model.SQUARE_SIZE, model.SQUARE_SIZE))
            elif event.name == "end":
                print("End needs to be drawn")
                pygame.draw.rect(self.screen, RED, (state.x, state.y, model.SQUARE_SIZE, model.SQUARE_SIZE))
            pygame.display.flip()

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
        self.init_grid()
