import pygame
import model
from eventmanager import *


class Keyboard(object):
    """
    Handles keyboard input.
    """

    def __init__(self, event_manager, model):
        """
        event_manager (EventManager): Allows posting messages to the event queue.
        model (GameEngine): a strong reference to the game Model.
        """
        self.__event_manager = event_manager
        self.__event_manager.RegisterListener(self)
        self.__model = model

    def notify(self, event):
        """
        Receive events posted to the message queue.
        """

        if isinstance(event, TickEvent):
            # Called for each game tick. We check our keyboard presses here.
            for event in pygame.event.get():
                # handle window manager closing our window
                if event.type == pygame.QUIT:
                    self.__event_manager.post(QuitEvent())
                # handle key down events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__event_manager.post(QuitEvent())
                    else:
                        # post any other keys to the message queue for everyone else to see
                        self.__event_manager.post(InputEvent(event.unicode, None))
