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
from colour import Color 

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(Sprite):

    def __init__(self, sprite_color, atk):

        def name_to_rgb(thiscolor):
            if type(thiscolor) != tuple:
                col = Color(thiscolor)
                lttup = []
                for x in col.rgb:
                    lttup.append(int(round(x * 255, 0)))
                lttup = tuple(lttup)
                thiscolor = lttup
                return thiscolor
            else:
                return thiscolor

        super(Player, self).__init__()
        self.surf = Surface((50, 50))
        thiscolor = name_to_rgb(sprite_color)
        self.surf.fill(thiscolor)
        self.rect = self.surf.get_rect()
        self.atk = atk
        self.allowjump = False
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
    
    def atk_stats(self): 
        if self.atk == 1:
            return 'rock'
        elif self.atk == 2:
            return 'paper'
        elif self.atk == 3:
            return 'scissors'

    def change_atk(self):
        if self.atk >= 3:
            self.atk = 1
        else: 
            self.atk += 1
            
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

# use w3c color naming to recognize them
player1 = Player('darkgreen', 3)
player2 = Player('darkmagenta', 1)
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
        else:
            if (player1.atk == 1 and player2.atk == 3) \
            or (player1.atk == 2 and player2.atk == 1) \
            or (player1.atk == 3 and player2.atk == 2):
                if sp1 == 0:
                    player2.speed.x = -sp2 * 2
                    player1.speed.x = 0
                else:
                    player2.speed.x = sp1 * 2
                    player1.speed.x = 0
            else:
                if sp1 == 0:
                    player1.speed.x = sp2 * 2
                    player2.speed.x = 0
                else:
                    player1.speed.x = -sp1 * 2
                    player2.speed.x = 0

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
            temp1 = player1.allowjump    
            player1.allowjump = True
            if (temp1 != player1.allowjump):
                print('player1: ' + str(player1.atk_stats()))
                player1.change_atk()
        else:
            player1.speed.y += 2
            player1.allowjump = False
    
    if player2.speed.y < 0:
        if (player2.rect.top <= 150):
            player2.speed.y = 0
    else:
        if pygame.sprite.collide_rect(player2, ground1):  # checks collision player to ground
            player2.speed.y = 0
            temp2 = player2.allowjump
            player2.allowjump = True
            if (temp2 != player2.allowjump):
                print('player2: ' + str(player2.atk_stats()))
                player2.change_atk()
        else:
            player2.speed.y += 2
            player2.allowjump = False

    if player1.rect.bottom > ground1.rect.top + 5:
        if pygame.sprite.collide_rect(player1, ground1):
            player1.speed.x = 0
            player1.speed.y += 2
            
    if player2.rect.bottom > ground1.rect.top + 5:
        if pygame.sprite.collide_rect(player2, ground1):
            player2.speed.x = 0
            player2.speed.y += 2
    
    player1.bound()
    player2.bound()

    player2.move()
    player1.move()

    screen.blit(player1.surf, player1.rect)
    screen.blit(player2.surf, player2.rect)

    pygame.display.flip()

pygame.quit()
