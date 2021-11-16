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
        self.__event_manager.register_listener(self)
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
                    self.__event_manager.Post(QuitEvent())
                # handle key down events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__event_manager.Post(StateChangeEvent(None))
                    else:
                        current_state = self.__model.state.peek()
                        # The user has yet to select the start and end squares
                        if current_state == model.StateType.SELECTION:
                            self.key_down_selection(event)
                        if current_state == model.StateType.RUNNING:
                            self.key_down_run(event)
                        # TODO
                        # if current_state == model.StateType.ENDED:
                        #     self.keydownhelp(event)
                        if current_state == model.StateType.PAUSED:
                            self.key_down_pause(event)

    def key_down_selection(self, event):
        """
        Handles menu key events.
        """

        # escape pops the menu
        if event.key == pygame.K_ESCAPE:
            self.__event_manager.Post(StateChangeEvent(None))
        # space plays the game
        # TODO: Only let state change to running occur once the user has picked the start and end nodes
        if event.key == pygame.K_SPACE:
            print("Running")
            self.__event_manager.Post(StateChangeEvent(model.StateType.RUNNING))

    def key_down_pause(self, event):
        """
        Handles help key events.
        """

        # space, enter or escape pops help
        if event.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
            self.__event_manager.Post(StateChangeEvent(None))

    def key_down_run(self, event):
        """
        Handles play key events.
        """

        if event.key == pygame.K_ESCAPE:
            self.__event_manager.Post(StateChangeEvent(None))
        # F1 pauses the game
        if event.key == pygame.K_F1:
            self.__event_manager.Post(StateChangeEvent(model.StateType.PAUSED))
        else:
            self.__event_manager.Post(InputEvent(event.unicode, None))