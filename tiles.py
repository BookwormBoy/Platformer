import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect=self.image.get_rect(topleft = pos)

        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0,0)
    def update(self, x_shift, y_shift):
        # self.acc = (x_shift, y_shift)
        # self.vel += self.acc
        
        self.pos.x += x_shift
        # print(x_shift, self.rect.x)
        self.pos.y += y_shift

        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)