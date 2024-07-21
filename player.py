import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index=0
        self.animation_speed=0.10
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.slide_rect = (self.rect.x, self.rect.y+12, self.rect.width+12, self.rect.height-12)
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.coords = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.walkspeed=3
        self.runacc=0.1
        self.rundec=0.2
        self.runspeed=8

        self.on_ground = True
        self.status='idle'
        self.jumped=False
        self.slow_jump=False
        self.facing_right=True
        self.touching_wall_l=False
        self.touching_wall_r=False
        self.sliding=False
        self.slowdown=False

    def import_character_assets(self):
        character_path='./graphics/character/'
        self.animations={'idle':[], 'walk':[], 'jump':[], 'fall':[], 'wall_slide':[], 'run':[], 'slide':[]}
        cx={'idle':14, 'jump':17, 'walk':21, 'fall':17, 'wall_slide':15, 'run': 17, 'slide':9}
        cy={'idle':6, 'jump':7, 'walk':7, 'fall':1, 'wall_slide':3, 'run':7, 'slide':19}
        w={'idle':19, 'jump':19, 'walk':19, 'fall':19, 'wall_slide':19, 'run': 19, 'slide':31}
        h={'idle':30, 'jump':30, 'walk':30, 'fall':30, 'wall_slide':30, 'run': 30, 'slide':18}


        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation]=import_folder(full_path, cx[animation], cy[animation], w[animation], h[animation])

    def get_input(self):
        keys = pygame.key.get_pressed()


        if self.vel.x==0:  #x-movement
            self.sliding=False
            if keys[pygame.K_RIGHT]:
                self.slowdown=False
                if keys[pygame.K_s]:
                    self.acc.x=self.runacc
                else:
                    self.vel.x=self.walkspeed
                    self.acc.x=0
            elif keys[pygame.K_LEFT]:
                self.slowdown=False
                if keys[pygame.K_s]:
                    self.acc.x=-self.runacc
                else:
                    self.vel.x=-self.walkspeed
                    self.acc.x=0
        elif (abs(self.vel.x))<=self.walkspeed:
            if self.sliding:
                if self.vel.x>0 and not keys[pygame.K_LEFT]:
                    self.sliding=False
                elif self.vel.x<0 and not keys[pygame.K_RIGHT]:
                    self.sliding=False
            else:
                if keys[pygame.K_RIGHT]:
                    self.slowdown=False
                    if keys[pygame.K_s]:
                        self.acc.x=self.runacc
                    else:
                        self.vel.x=self.walkspeed
                        self.acc.x=0
                elif keys[pygame.K_LEFT]:
                    self.slowdown=False
                    if keys[pygame.K_s]:
                        self.acc.x=-self.runacc
                    else:
                        self.vel.x=-self.walkspeed
                        self.acc.x=0
                else:
                    self.vel.x=0
        else:
            if self.sliding:
                if self.vel.x>0 and not keys[pygame.K_LEFT]:
                    self.sliding=False
                elif self.vel.x<0 and not keys[pygame.K_RIGHT]:
                    self.sliding=False
            else:
                if keys[pygame.K_s]:
                    if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
                        if keys[pygame.K_RIGHT] and self.vel.x<0:
                            self.sliding=True
                            self.slowdown=True
                        elif keys[pygame.K_RIGHT] and self.vel.x>0:
                            self.slowdown=False
                            self.acc.x=self.runacc
                        elif keys[pygame.K_LEFT] and self.vel.x>0:
                            self.sliding=True
                            self.slowdown=True
                        elif keys[pygame.K_LEFT] and self.vel.x<0:
                            self.slowdown=False
                            self.acc.x=-self.runacc
                    else:
                        self.slowdown=True
                else:
                    self.slowdown=True

        if not self.on_ground:
            self.sliding=False

        if self.slowdown:
            if(self.vel.x>0.1):
                self.acc.x = -self.rundec
            elif(self.vel.x<-0.1):
                self.acc.x = self.rundec
            else:
                self.acc.x=0
                self.vel.x=0


        # print(self.acc.x, self.vel.x, self.sliding, self.slowdown)
                          

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

        if keys[pygame.K_c] and self.status=='wall_slide':
            self.vel.y-=25
            if self.touching_wall_r:
                self.vel.x-=15
            elif self.touching_wall_l:
                self.vel.x+=15
        


    def get_status(self):

        keys = pygame.key.get_pressed()

        if self.on_ground:
            if self.touching_wall_l or self.touching_wall_r:
                self.status='idle'
            else:
                if self.vel.x==0:
                    self.status='idle'
                else:
                    if self.sliding:
                        self.status='slide'
                    else:
                        if abs(self.vel.x)<=self.walkspeed:
                            self.status='walk'
                        else:
                            self.status='run'
        else:
            if self.vel.y>=0:
                if self.touching_wall_l or self.touching_wall_r:
                    if self.touching_wall_l and keys[pygame.K_LEFT]:
                        self.status='wall_slide'
                    elif self.touching_wall_r and keys[pygame.K_RIGHT]:
                        self.status='wall_slide'
                    else:
                        self.status='fall'
                else:
                    self.status='fall'
            else:
                self.status='jump'

        if self.touching_wall_l and keys[pygame.K_RIGHT]:
            self.touching_wall_l=False

        if self.touching_wall_r and keys[pygame.K_LEFT]:
            self.touching_wall_r=False

        # print(self.touching_wall_r)

        # print(self.status, self.vel.x)

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
        self.slide_rect = (self.rect.x, self.rect.y+12, self.rect.width+12, self.rect.height-12)

        
        
        

    