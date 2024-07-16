import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index=0
        self.animation_speed=0.05
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.coords = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

        self.on_ground = True
        self.status='idle'
        self.jumped=False
        self.slow_jump=False
        self.facing_right=True

    def import_character_assets(self):
        character_path='/home/siddharth-kini/Platformer/graphics/character/'
        self.animations={'idle':[], 'walk':[], 'jump':[], 'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation]=import_folder(full_path)

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

        if self.vel.x>0:
            self.facing_right=True
        elif self.vel.x<0:
            self.facing_right=False

        if keys[pygame.K_c] and self.on_ground: #jump
            self.jumped=True
            self.vel.y = -17

        if keys[pygame.K_c] and self.jumped:
            self.slow_jump=True
        else:
            self.slow_jump=False
        


    def get_status(self):

        keys = pygame.key.get_pressed()

        if(self.status=='jump' and self.vel.y>=0):
            self.status='fall'
        elif(self.vel.y>1):
            self.status='fall'
        elif(self.vel.y<0):
            self.status='jump'
        else:
            if(self.vel.x!=0):
                self.status='walk'
            else:
                self.status='idle'

        # print(self.status)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index+=self.animation_speed
        if self.frame_index >= len(animation):
            if(self.status=='fall' or self.status=='jump'):
                self.frame_index=len(animation)-1
            self.frame_index=0

        image=animation[int(self.frame_index)]
        if self.facing_right:
            self.image=image
        else:
            flipped_image=pygame.transform.flip(image, True, False)
            self.image=flipped_image

    def update(self):

        self.get_input()
        self.get_status()
        self.animate()
        
        
        

    