import pygame
import model
from eventmanager import *


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
        self.__event_manager.RegisterListener(self)
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
            self.render_all()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(30)

    def render_all(self):
        """
        Draw the current game state on screen.
        Does nothing if is_initialized == False (pygame.init failed)
        """

        if not self.is_initialized:
            return
        # clear display
        self.screen.fill((0, 0, 0))
        # draw some words on the screen
        some_words = self.small_font.render(
            'The View is busy drawing on your screen',
            True,
            (0, 255, 0))
        self.screen.blit(some_words, (0, 0))
        # flip the display to show whatever we drew
        pygame.display.flip()

    def initialize(self):
        """
        Set up the pygame graphical display and loads graphical resources.
        """

        result = pygame.init()
        pygame.font.init()
        pygame.display.set_caption('demo game')
        self.screen = pygame.display.set_mode((600, 60))
        self.clock = pygame.time.Clock()
        self.small_font = pygame.font.Font(None, 40)
        self.is_initialized = True
