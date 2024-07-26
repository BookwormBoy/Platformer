import pygame
import math

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect=self.image.get_rect(topleft = pos)

        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.coords = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0,0)
    def update(self, x_shift, y_shift):
        # self.acc = (x_shift, y_shift)
        # self.vel += self.acc
        
        self.pos.x += x_shift
        # print('x', self.rect.x)
        self.pos.y += y_shift
        

        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

class H_Moving_Platform(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pygame.Surface((size*3, size))
        self.image.fill('blue')
        self.rect=self.image.get_rect(topleft = pos)
        self.w=0.003
        self.amp=1000
    
    def move(self):
        t=pygame.time.get_ticks()
        self.vel.x = -self.amp*self.w*math.sin(self.w*t)
        self.pos.x+=self.vel.x
        self.coords.x+=self.vel.x
        # print(self.rect.x)

class Canon(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pygame.Surface((size, size))
        self.image.fill('blue')
        self.freq=120

class Bullet(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pygame.Surface((30, 10))
        self.image.fill('green')
        self.rect=self.image.get_rect(topleft=pos)

        self.bounced_on=False

    def move_x(self):
        self.pos.x-=2
        self.coords.x-=2
        self.rect.x = int(self.pos.x)

    def move_y(self):

        if self.bounced_on:
            self.acc.y=0.2

        self.vel.y+=self.acc.y
        self.pos.y+=self.vel.y
        self.coords.y+=self.vel.y
        self.rect.y=int(self.pos.y)

class On_Off_Switch(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image.fill('purple')

    def change_sprite(self, on):
        if on:
            self.image.fill('purple')
        else:
            self.image.fill('blue')

class On_Block(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image.fill('purple')

    def change_sprite(self, on):
        if on:
            self.image.fill('purple')
        else:
            self.image.fill('pink')

class Off_Block(Tile):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image.fill('light blue')

    def change_sprite(self, on):
        if on:
            self.image.fill('light blue')
        else:
            self.image.fill('blue')

class Shell(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill('grey')
        self.rect=self.image.get_rect(topleft = pos)

        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.coords = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0,0.6)

        self.kicked=False

    def move_x(self, shift):
        self.vel.x+=self.acc.x
        self.pos.x+=shift
        self.pos.x+=self.vel.x
        self.coords.x+=self.vel.x
        self.rect.x=int(self.pos.x)

    def move_y(self, shift):
        self.vel.y+=self.acc.y
        self.pos.y+=shift
        self.pos.y+=self.vel.y
        self.coords.y+=self.vel.y
        self.rect.y=int(self.pos.y)


