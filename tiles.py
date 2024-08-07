import pygame
import math

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos,coords, surface):
        super().__init__()
        self.image = surface
        self.rect=self.image.get_rect(topleft = pos)

        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.coords = pygame.math.Vector2(coords[0], coords[1])
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

class Bg_Tile(Tile):
    def __init__(self, pos, coords, surface):
        super().__init__(pos, coords, surface)

class H_Moving_Platform(Tile):
    def __init__(self, pos,coords, surface):
        super().__init__(pos,coords, surface)
        self.w=0.002
        self.amp=1800
    
    def move(self):
        t=pygame.time.get_ticks()
        self.vel.x = -self.amp*self.w*math.sin(self.w*t)
        self.pos.x+=self.vel.x
        self.coords.x+=self.vel.x
        # print(self.rect.x)

class Canon(Tile):
    def __init__(self, pos, coords,surface):
        super().__init__(pos, coords,surface)
        self.freq=120

class Bullet(Tile):
    def __init__(self, pos,coords, surface):
        super().__init__(pos, coords, surface)
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
    def __init__(self, pos, coords,size):
        super().__init__(pos, coords, size)
        self.image.fill('purple')

    def change_sprite(self, on):
        if on:
            self.image.fill('purple')
        else:
            self.image.fill('blue')

class On_Block(Tile):
    def __init__(self, pos, coords, size):
        super().__init__(pos,coords, size)
        self.image.fill('purple')

    def change_sprite(self, on):
        if on:
            self.image.fill('purple')
        else:
            self.image.fill('pink')

class Off_Block(Tile):
    def __init__(self, pos, coords,size):
        super().__init__(pos, coords, size)
        self.image.fill('light blue')

    def change_sprite(self, on):
        if on:
            self.image.fill('light blue')
        else:
            self.image.fill('blue')

class Shell(pygame.sprite.Sprite):
    def __init__(self, coords,pos):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill('grey')
        self.rect=self.image.get_rect(topleft = pos)

        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.coords = pygame.math.Vector2(coords[0], coords[1])
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0,0.6)

        self.kicked=False
        self.held=False

    def move_x(self, shift, player_x, player_coords):
        self.vel.x+=self.acc.x

        if self.held:
            self.pos.x=player_x
            self.coords.x=player_coords
        else:
            self.pos.x+=shift
            self.pos.x+=self.vel.x
            self.coords.x+=self.vel.x
        self.rect.x=int(self.pos.x)


    def move_y(self, shift, player_y, player_coords):
        self.vel.y+=self.acc.y

        if self.held:
            self.pos.y=player_y
            self.coords.y=player_coords
        else:
            self.pos.y+=shift
            self.pos.y+=self.vel.y
            self.coords.y+=self.vel.y
        self.rect.y=int(self.pos.y)

class Falling_Platform(Tile):
    def __init__(self, pos, coords,surface):
        super().__init__(pos,coords, surface)
        self.triggered=False

    def move(self):
        if self.triggered:
            self.acc.y=0.1
            self.vel.y+=self.acc.y
            self.pos.y+=self.vel.y
            self.rect.y=int(self.pos.y)

class Spike(Tile):
    def __init__(self, pos, coords,surface):
        super().__init__(pos, coords,surface)

class Firejet(Tile):
    def __init__(self, pos, coords,size):
        super().__init__(pos, coords,size)
        self.image.fill('blue')

class Flame(pygame.sprite.Sprite):
    def __init__(self, pos, coords,size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect=self.image.get_rect(topleft = pos)

        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.coords = pygame.math.Vector2(coords[0], coords[1])
        self.image.fill('red')
        self.on=True
        self.freq=200

    def move_x(self, shift):
        self.pos.x+=shift
        self.coords.x+=shift
        self.rect.x=int(self.pos.x)

    def move_y(self, shift):
        self.pos.y+=shift
        self.coords.y+=shift
        self.rect.y=int(self.pos.y)

class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, pos, coords,surface):
        super().__init__()
        self.image = surface
        self.rect=self.image.get_rect(topleft = pos)

        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.coords = pygame.math.Vector2(coords[0], coords[1])

    def move_x(self, shift):
        self.pos.x+=shift
        self.rect.x=int(self.pos.x)

    def move_y(self, shift):
        self.pos.y+=shift
        self.rect.y=int(self.pos.y)

class Falling_Spike(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect=self.image.get_rect(topleft = pos)

        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.vel=0
        self.acc=0.2

    def update(self):
        self.vel+=self.acc
        self.pos.y+=self.vel
        self.rect.y=int(self.pos.y)
    





