import pygame


class EventHandler:
    targets = {}

    @staticmethod
    def add(type, event):
        EventHandler.targets.setdefault(type, []).append(event)

    @staticmethod
    def notify(event):
        if event.type in EventHandler.targets:
            for target in EventHandler.targets[event.type]:
                target.determine_event(event)

    @staticmethod
    def determine_event(event):
        pass


class Exit(EventHandler):
    @staticmethod
    def determine_event(event):
        pygame.quit()
        quit(0)


class KeydownPrint(EventHandler):
    @staticmethod
    def determine_event(event):
        print(event.key)


class KeydownAction(EventHandler):
    @staticmethod
    def determine_event(event):
        print("action")


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


EventHandler.add(pygame.QUIT, Exit)
EventHandler.add(pygame.KEYDOWN, KeydownPrint)
EventHandler.add(pygame.KEYDOWN, KeydownAction)

while True:
    for event in pygame.event.get():
        EventHandler.notify(event)
