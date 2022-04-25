import pygame
from pygame.display import (
    set_caption,
    set_icon,
    set_mode
)
from pygame.surface import Surface
from pygame.sprite import Sprite
from pygame.image import load
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_a,
    K_s,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from pygame import Vector2
from pprint import pp
from PySide2.examples.multimedia import player

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# (0,0,0) tuple black color


class Player(Sprite):

    def __init__(self, sprite_color, atk):
        super(Player, self).__init__()
        self.surf = Surface((50, 50))
        self.surf.fill(sprite_color)
        self.rect = self.surf.get_rect()
        self.atk = atk
        self.allowjump = False
        
        if self.atk == 1:
            print('rock')
        elif self.atk == 2:
            print('paper')
        elif self.atk == 3:
            print('scissors')
            
        self.speed = pygame.Vector2()
        
    def update_player1(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.speed.x = -1
    
        if pressed_keys[K_RIGHT]:
            self.speed.x = 1
         
        if pressed_keys[K_UP] and self.allowjump == True:
            self.speed.y += -0.3
        else: 
            self.speed.y = 0  
                
        if pressed_keys[K_DOWN]:
            self.speed.x = 0
    
    def update_player2(self, pressed_keys):
        if pressed_keys[K_a]:
            self.speed.x = -1
    
        if pressed_keys[K_d]:
            self.speed.x = 1

        if pressed_keys[K_w] and self.allowjump == True:
            self.speed.y += -0.3
        else: 
            self.speed.y = 0
    
        if pressed_keys[K_s]:
            if (self.speed.x > 0):
                self.speed.x = 0
        
    def move(self):
        self.rect.move_ip(self.speed)
        
    def bound(self):
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.speed.y = 0

        if self.rect.left < 0:
            self.rect.left = 0


class Ground(Sprite):

    def __init__(self):
        super(Ground, self).__init__()
        self.surf = Surface((600, 200))
        self.surf.fill((200, 0, 0))
        self.rect = self.surf.get_rect(center=((400), (500)))


icon = load('./assets/icon.png')

pygame.init()

# Window/Screen
screen = set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
set_caption("rock paper scissors")
set_icon(icon)

player1 = Player((43, 224, 179), 1)
player2 = Player((43, 109, 224), 1)
ground1 = Ground()

player2.rect.move_ip(177, 100)
player1.rect.move_ip(599, 100)

running = True

while running:
    screen.fill((255, 255, 255))
    screen.blit(ground1.surf, ground1.rect)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player1.update_player1(pressed_keys)
    player2.update_player2(pressed_keys)

# EXPERIMENTAL / UNFINISHED
    def sign(num):
        if num < 0:
            return -1
        elif num > 0:
            return 1
        else:
            return 0

    sp1 = sign(player1.speed.x)
    sp2 = sign(player2.speed.x)
    
    if pygame.sprite.collide_rect(player1, player2): 
        if (player1.atk == player2.atk):
            if sp1 == 0:
                player2.speed.x = -sp2 * 2
                player1.speed.x = -player2.speed.x
            else:
                player1.speed.x = -sp1 * 2
                player2.speed.x = -player1.speed.x

#      r p s
#    r x l w
#    p w x l
#    s l w x

# <rect(177, 400, 50, 50)>
# <rect(594, 400, 50, 50)>    
    # player1.gravity()
    # player2.gravity()
    
        # # New gravity realistic
        
    if player1.speed.y < 0:
        if (player1.rect.top <= 150):
            player1.speed.y = 0
    else:
        if pygame.sprite.collide_rect(player1, ground1):  # checks collision player to ground
            player1.speed.y = 0
            player1.allowjump = True
        else:
            player1.speed.y += 2
            player1.allowjump = False
            
    if player2.speed.y < 0:
        if (player2.rect.top <= 150):
            player2.speed.y = 0
    else:
        if pygame.sprite.collide_rect(player2, ground1):  # checks collision player to ground
            player2.speed.y = 0
            player2.allowjump = True
        else:
            player2.speed.y += 2
            player2.allowjump = False
   
    player1.bound()
    player2.bound()

    player2.move()
    player1.move()

    screen.blit(player1.surf, player1.rect)
    screen.blit(player2.surf, player2.rect)

    pygame.display.flip()

pygame.quit()
