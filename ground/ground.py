from pygame.sprite import Sprite
import pygame

class Ground(Sprite):

    def __init__(self):
        super(Ground, self).__init__()
        #self.surf = Surface((550, 100))
        #self.surf.fill((200, 0, 0))
        self.surf = pygame.image.load("./assets/table.jpeg").convert()
        self.rect = self.surf.get_rect(center=((400), (470)))
