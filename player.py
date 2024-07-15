import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((50, 100))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.coords = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

        self.on_ground = True
        self.status='idle'
        self.jumped=False
        self.slow_jump=False

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]: #x movement
            self.acc.x = 0.1
        elif keys[pygame.K_LEFT]:
            self.acc.x = -0.1
        else:
            if(self.vel.x>0.1):
                self.acc.x = -0.1
            elif(self.vel.x<-0.1):
                self.acc.x = 0.1
            else:
                self.acc.x=0
                self.vel.x=0

        if keys[pygame.K_c] and self.on_ground: #jump
            self.jumped=True
            self.vel.y = -17

        if keys[pygame.K_c] and self.jumped:
            self.slow_jump=True
        else:
            self.slow_jump=False
        


    def get_status(self):

        keys = pygame.key.get_pressed()

        if(self.vel.y>0):
            self.status='jump'

    def update(self):
        self.get_input()

        
        
        

    