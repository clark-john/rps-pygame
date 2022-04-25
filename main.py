import pygame
from colour import Color
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

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# (0,0,0) tuple black color

class Player(Sprite):
    def __init__(self, sprite_color, atk):
        super(Player, self).__init__()

        # -------------------------
        def name_to_rgb(thiscolor):
            if type(thiscolor) != tuple:
                print("not tuple")
                col = Color(thiscolor)
                lttup = []
                for x in col.rgb:
                    lttup.append(int(round(x*255,0)))
                lttup = tuple(lttup)
                thiscolor = lttup
                return thiscolor
            else:
                return thiscolor
        # ------------------------
        
        thiscolor = name_to_rgb(sprite_color)
        self.surf = Surface((50, 50))
        self.surf.fill(thiscolor)
        self.rect = self.surf.get_rect()
        if atk == 1:
            print('scissors')
        elif atk == 2:
            print('paper')
        elif atk == 3:
            print('rock')

    def update_player1(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -6)

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 6)

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-3, 0)

        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(3, 0)

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        if self.rect.left < 0:
            self.rect.left = 0

    def update_player2(self, pressed_keys):

        if pressed_keys[K_w]:
            self.rect.move_ip(0, -6)

        if pressed_keys[K_s]:
            self.rect.move_ip(0, 6)

        if pressed_keys[K_a]:
            self.rect.move_ip(-3, 0)

        if pressed_keys[K_d]:
            self.rect.move_ip(3, 0)

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        
    def gravity(self):
        self.rect.bottom += 3

class Ground(Sprite):
    def __init__(self):
        super(Ground, self).__init__()
        self.surf = Surface((600, 200))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center=((400),(500)))

icon = load('./assets/icon.png')

pygame.init()

# Window/Screen
screen = set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
set_caption("rock paper scissors")
set_icon(icon)

player1 = Player('red',1)
player2 = Player((43, 224, 179),1)
ground1 = Ground()

player1.rect.move_ip(177, 100)
player2.rect.move_ip(599, 100)

running = True

while running:
    # for loop through the event queue
    for event in pygame.event.get():

        # Check for KEYDOWN event
        if event.type == KEYDOWN:

            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False

        # Check for QUIT event. If QUIT, then set running to false.

        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    
    player1.update_player1(pressed_keys)
    player2.update_player2(pressed_keys)

    screen.fill((255, 255, 255))

    # Fighting ground
    screen.blit(ground1.surf, ground1.rect)

    
    #boolean to check if player1 is above fground
    pl_above_fground = player1.rect.bottom >= ground1.rect.top
    
    
    if pygame.sprite.collide_rect(player1, ground1):  
        if player1.rect.right <= ground1.rect.right:
            if player1.rect.left <= ground1.rect.left:
               player1.rect.right = ground1.rect.left
            else: player1.rect.bottom = ground1.rect.top
        else: player1.rect.left = ground1.rect.right
    
    if pygame.sprite.collide_rect(player2, ground1):            #checks collision player to ground
        if player2.rect.right <= ground1.rect.right:            #checks if within right end
            if player2.rect.left > ground1.rect.left:           #checks if with left end
               player2.rect.bottom = ground1.rect.top           #stays on top of the ground
            else: player2.rect.right = ground1.rect.left        #bounded by ground's left side
        else: player2.rect.left = ground1.rect.right            #bounded by ground's right side
    
    if pygame.sprite.collide_rect(player2, player1):
        print('players collided')
      #  break

# <rect(177, 400, 50, 50)>
# <rect(594, 400, 50, 50)>    
    player1.gravity();
    player2.gravity();

    screen.blit(player1.surf, player1.rect)
    screen.blit(player2.surf, player2.rect)

    # print(player2.rect)
    # print(player1.rect)
    pygame.display.flip()

pygame.quit()
