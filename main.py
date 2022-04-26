import pygame
from pygame.display import set_caption, set_icon, set_mode
from pygame.surface import Surface
from pygame.sprite import Sprite
from pygame.image import load
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_a,K_s,K_d,K_w,K_LEFT,K_RIGHT,K_UP,K_DOWN
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
)
player2 = Player(
    "darkmagenta",
    attack.AttackType.ROCK,
    Controller(left=K_a, right=K_d, up=K_w, down=K_s),
)
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
    player2.update_player1(pressed_keys)

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
        if player1.atk == player2.atk:
            if sp1 == 0:
                player2.speed.x = -sp2 * 2
                player1.speed.x = -player2.speed.x
            else:
                player1.speed.x = -sp1 * 2
                player2.speed.x = -player1.speed.x
        else:
            if (
                (player1.atk == 1 and player2.atk == 3)
                or (player1.atk == 2 and player2.atk == 1)
                or (player1.atk == 3 and player2.atk == 2)
            ):
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
        if player1.rect.top <= 150:
            player1.speed.y = 0
    else:
        if pygame.sprite.collide_rect(
            player1, ground1
        ):  # checks collision player to ground
            player1.speed.y = 0
            temp1 = player1.allowjump
            player1.allowjump = True
            if temp1 != player1.allowjump:
                print("player1: " + str(player1.atk_stats()))
                player1.change_atk()
        else:
            player1.speed.y += 2
            player1.allowjump = False

    if player2.speed.y < 0:
        if player2.rect.top <= 150:
            player2.speed.y = 0
    else:
        if pygame.sprite.collide_rect(
            player2, ground1
        ):  # checks collision player to ground
            player2.speed.y = 0
            temp2 = player2.allowjump
            player2.allowjump = True
            if temp2 != player2.allowjump:
                print("player2: " + str(player2.atk_stats()))
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
