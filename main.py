import pygame
from pygame.display import set_caption, set_icon, set_mode
from pygame.surface import Surface
from pygame.sprite import Sprite
from pygame.image import load
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_a,K_s,K_d,K_w,K_LEFT,K_RIGHT,K_UP,K_DOWN, K_r
)
from colour import Color
from player.player import Player
from ground.ground import Ground
from core import constants, attack
from controller.controller import Controller


icon = load("./assets/icon.png")

pygame.init()

# Window/Screen
screen = set_mode([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])
set_caption("rock paper scissors")
set_icon(icon)

# use w3c color naming to recognize them
player1 = Player(
    "darkgreen",
    attack.AttackType.SCISSORS,
    Controller(left=K_LEFT, right=K_RIGHT, up=K_UP, down=K_DOWN),
    (599, 100)
)
player2 = Player(
    "darkmagenta",
    attack.AttackType.SCISSORS,
    Controller(left=K_a, right=K_d, up=K_w, down=K_s),
    (177,100)
)
ground1 = Ground()

running = True

while running:
    screen.fill((255, 255, 128, 255))
    screen.blit(ground1.surf, ground1.rect)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player1.update(pressed_keys)
    player2.update(pressed_keys)

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
                player2.speed.x = -sp2 * 3
                player1.speed.x = -player2.speed.x
            else:
                player1.speed.x = -sp1 * 3
                player2.speed.x = -player1.speed.x
        else:
            if (player1.atk == 1 and player2.atk == 3) \
            or (player1.atk == 2 and player2.atk == 1) \
            or (player1.atk == 3 and player2.atk == 2):
                if sp1 == 0:
                    player2.speed.x = -sp2 * 3
                    player1.speed.x = 0
                else:
                    player2.speed.x = sp1 * 3
                    player1.speed.x = 0
            else:
                if sp1 == 0:
                    player1.speed.x = sp2 * 3
                    player2.speed.x = 0
                else:
                    player1.speed.x = -sp1 * 3
                    player2.speed.x = 0

        #      r p s
        #    r x l w
        #    p w x l
        #    s l w x
 
    if player1.speed.y < 0:
        if pygame.sprite.collide_rect(player1, player2):
            if not (pygame.sprite.collide_rect(player1, ground1) or pygame.sprite.collide_rect(player2, ground1)):
                player1.speed.y += 3
        else: 
            if (player1.rect.top <= 100):
                player1.speed.y = 0
    else:
        if pygame.sprite.collide_rect(player1, ground1):  # checks collision player to ground
            player1.speed.y = 0
            temp1 = player1.allowjump
            player1.allowjump = True
            if (temp1 != player1.allowjump):
                #print('player1: ' + str(player1.atk_stats()))
                player1.change_atk()
        else:
            player1.speed.y += 0.02
            #print(str(player1.speed))
            player1.allowjump = False
    
    if player2.speed.y < 0:
        if pygame.sprite.collide_rect(player1, player2):
            if not (pygame.sprite.collide_rect(player1, ground1) or pygame.sprite.collide_rect(player2, ground1)):
                player2.speed.y += 3
        else: 
            if (player2.rect.top <= 100):
                player2.speed.y = 0
    else:
        if pygame.sprite.collide_rect(player2, ground1):  # checks collision player to ground
            player2.speed.y = 0
            temp2 = player2.allowjump
            player2.allowjump = True
            if (temp2 != player2.allowjump):
                #print('player2: ' + str(player2.atk_stats()))
                player2.change_atk()
        else:
            player2.speed.y += 0.02
            #print(str(player2.speed))
            player2.allowjump = False
    
    # disables player flying upwards when below ground

    if pygame.sprite.collide_rect(player1, ground1):
        if player1.rect.bottom > ground1.rect.top + 10:
            player1.speed.x = 0
            player1.speed.y += 2
        
    if pygame.sprite.collide_rect(player2, ground1):
        if player2.rect.bottom > ground1.rect.top + 10:
            player2.speed.x = 0
            player2.speed.y += 2

    if player1.bound() or player2.bound():
        player2.reset_pos()
        player1.reset_pos()

    player2.move()
    player1.move()
    
    
    #screen.blit(player1.surf, player1.rect)
    #screen.blit(player2.surf, player2.rect)
    screen.blit(player1.image, player1.rect)
    screen.blit(player2.image, player2.rect)
    pygame.display.flip()

pygame.quit()
