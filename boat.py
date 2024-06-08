import pygame, os

class Boat2():
    def __init__(self) -> None:
        self.image = pygame.image.load('graphics/fruit/inventory.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100)) 
        self.rect = self.image.get_rect()

    def display(self, surface):
        # color = (255,0,0)
        # pygame.draw.rect(surface, color, pygame.Rect(1000, 100, 60, 60),  2)
        # pygame.display.flip()
        surface.blit(self.image, (0, 0))

class Boat():
    def __init__(self, pos) -> None:
        self.pos = pos
        # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
        self.image = pygame.image.load('graphics/fruit/inventory.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100)) 
        self.rect = self.image.get_rect()

    def display(self, surface):
        # color = (255,0,0)
        # pygame.draw.rect(surface, color, pygame.Rect(1000, 100, 60, 60),  2)
        # pygame.display.flip()
        surface.blit(self.image, (self.pos))
        # print(os.environ['SDL_VIDEO_WINDOW_POS'])