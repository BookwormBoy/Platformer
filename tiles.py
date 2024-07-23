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

        

    def move(self):
        self.pos.x-=2
        self.coords.x-=2
        self.rect.x = int(self.pos.x)