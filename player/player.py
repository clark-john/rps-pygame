import pygame
from pygame.sprite import Sprite
from colour import Color
from tkinter import messagebox as msg
from core.attack import AttackType
from core.constants import SCREEN_HEIGHT,SCREEN_WIDTH
from controller.controller import Controller

class Player(Sprite):

    def __init__(self, sprite_color, atk:AttackType, controller:Controller, init_pos):
        def name_to_rgb(thiscolor):
            if type(thiscolor) != tuple:
                col = Color(thiscolor)
                lttup = []
                for x in col.rgb:
                    lttup.append(int(round(x * 255, 0)))
                lttup = tuple(lttup)
                thiscolor = lttup
            return thiscolor
                
        super(Player, self).__init__()
        self.controller = controller
        """ 
        self.surf = Surface((50, 50))
        thiscolor = name_to_rgb(sprite_color)
        self.surf.fill(thiscolor)
        self.rect = self.surf.get_rect() 
        """

        self.image = pygame.image.load("./assets/scissors.png").convert()
        
        # return a width and height of an image
        self.size = self.image.get_size()
        
        # create a smaller image than self.image
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.3), int(self.size[1]*0.3)))
        self.rect = self.image.get_rect() 

        self.atk = atk
        self.allowjump = False
        self.speed = pygame.Vector2()
        self.init_pos = init_pos
        print(self.init_pos)
        self.rect.move_ip(self.init_pos[0],self.init_pos[1])
        
    def update(self, pressed_keys):
        if pressed_keys[self.controller.left]:
            self.speed.x = -1
    
        if pressed_keys[self.controller.right]:
            self.speed.x = 1
         
        if pressed_keys[self.controller.up] and self.allowjump == True:
            self.speed.y -= 0.5

        if pressed_keys[self.controller.down]:
            self.speed.x = 0
  
    def move(self):
        self.rect.move_ip(self.speed)
        
    def reset_pos(self):
        self.speed.xy = (0,0)
        self.rect.x = self.init_pos[0]
        self.rect.y = self.init_pos[1]
        
    def bound(self):
        if self.rect.right > SCREEN_WIDTH:
            self.speed.x -= 0.3

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= SCREEN_HEIGHT:

            print("bottom of the screen")
            restart = msg.askyesno("rps-pygame","Play game again?")
            if restart:
                return True
            else:
                exit()
                
        if self.rect.left < 0:
            self.speed.x += 0.3
    
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

        if self.atk == AttackType.ROCK:
            self.image = pygame.image.load("./assets/rock.png").convert()
            # return a width and height of an image
            self.size = self.image.get_size()
            
            # create a 2x bigger image than self.image
            self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.3), int(self.size[1]*0.3)))
       
        elif self.atk == AttackType.PAPER:
            self.image = pygame.image.load("./assets/paper.png").convert()
            # return a width and height of an image
            self.size = self.image.get_size()
            
            # create a 2x bigger image than self.image
            self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.3), int(self.size[1]*0.3)))
        
        elif self.atk == AttackType.SCISSORS:
            self.image = pygame.image.load("./assets/scissors.png").convert()
            # return a width and height of an image
            self.size = self.image.get_size()
            
            # create a 2x bigger image than self.image
            self.image = pygame.transform.scale(self.image, (int(self.size[0]*0.3), int(self.size[1]*0.3)))
            
