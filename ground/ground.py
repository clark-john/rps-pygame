from pygame.sprite import Sprite
from pygame.surface import Surface


class Ground(Sprite):

    def __init__(self):
        super(Ground, self).__init__()
        self.surf = Surface((600, 20))
        self.surf.fill((200, 0, 0))
        self.rect = self.surf.get_rect(center=((400), (500)))
