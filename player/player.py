import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame import init
from colour import Color
from tkinter import messagebox as msg
from core.attack import AttackType
from core.constants import SCREEN_HEIGHT,SCREEN_WIDTH
from controller.controller import Controller

class Player(Sprite):

    def __init__(self, sprite_color, atk:AttackType, controller:Controller):
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
        self.controller = controller
        self.surf = Surface((50, 50))
        thiscolor = name_to_rgb(sprite_color)
        self.surf.fill(thiscolor)
        self.rect = self.surf.get_rect()
        self.atk = atk
        self.allowjump = False
        self.speed = pygame.Vector2()
        
    def update(self, pressed_keys):
        if pressed_keys[self.controller.left]:
            self.speed.x = -1
    
        if pressed_keys[self.controller.right]:
            self.speed.x = 1
         
        if pressed_keys[self.controller.up] and self.allowjump == True:
            self.speed.y += -0.3
        else: 
            self.speed.y = 0  
                
        if pressed_keys[self.controller.down]:
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
            print("bottom of the screen")
            restart = msg.askyesno("rps-pygame","Play game again?")
            if restart:
                self.rect.move_ip(self.speed)
            else:
                exit()

        if self.rect.left < 0:
            self.rect.left = 0
    
    def atk_stats(self): 
        if self.atk == AttackType.ROCK:
            return 'rock'
        elif self.atk == AttackType.PAPER:
            return 'paper'
        elif self.atk == AttackType.SCISSORS:
            return 'scissors'

    def change_atk(self):
        if self.atk >= AttackType.SCISSORS:
            self.atk = AttackType.ROCK
        else: 
            self.atk += 1