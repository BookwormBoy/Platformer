import pygame
from support  import *

class Ninja(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index=0
        self.animation_speed=0.18
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.vel = pygame.math.Vector2(0, 0)
        self.status='idle'
        self.idle_timer=0
        self.facing_right=False
        self.attacking=False
        self.has_attacked=False
        self.health=100
        self.dead=False

    def import_character_assets(self):
        character_path='./graphics/ninja/'
        self.animations={'idle':[], 'walk':[], 'attack':[], 'dead':[]}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation]=import_folder(full_path, 0, 0, 128, 128)

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index+=self.animation_speed
        if self.frame_index >= len(animation):
            if self.status=='dead':
                self.frame_index=len(animation)-1
            elif(self.status=='attack'):
                self.status='idle'
                self.frame_index=0
                self.idle_timer=pygame.time.get_ticks()
                self.attacking=False
                self.has_attacked=False
            else:
                self.frame_index=0

        image=animation[int(self.frame_index)]
        if self.facing_right:
            self.image=image
        else:
            flipped_image=pygame.transform.flip(image, True, False)
            self.image=flipped_image

        # print(self.frame_index, self.status, len(animation))


    def update(self, player):
        t=pygame.time.get_ticks()

        if self.status=='dead':
            return

        if self.health<=0:
            self.dead=True
            self.status='dead'
            self.frame_index=0
            self.animation_speed=0.15
            return
        if self.status=='idle' and t-self.idle_timer>1000:
            self.frame_index=0
            self.status='walk'

            if player.rect.centerx<self.rect.centerx:
                self.vel.x=-4
                self.facing_right=False
            elif player.rect.centerx>self.rect.centerx:
                self.vel.x=4
                self.facing_right=True

        elif self.status=='walk':
            if self.facing_right:
                if player.rect.centerx<self.rect.centerx:
                    self.frame_index=0
                    self.vel.x=0
                    self.status='idle'
                    self.idle_timer=pygame.time.get_ticks()
                else:
                    if ((player.rect.x+player.rect.width)>=(self.rect.x+104)) and (player.rect.x<=self.rect.x+236):
                        self.frame_index=0
                        self.vel.x=0
                        self.status='attack'
                        self.attacking=True
            else:
                if player.rect.centerx>self.rect.centerx:
                    self.frame_index=0
                    self.status='idle'
                    self.vel.x=0
                    self.idle_timer=pygame.time.get_ticks()
                else:
                    if ((player.rect.x+player.rect.width)>=(self.rect.x+20)) and (player.rect.x<=self.rect.x+152):
                        self.frame_index=0
                        self.vel.x=0
                        self.status='attack'
                        self.attacking=True

        self.pos.x+=self.vel.x
        self.rect.x=int(self.pos.x)
        # print(self.rect.x,self.rect.x+self.rect.width, player.rect.x, player.rect.x+player.rect.width)

    def handle_player_collisions(self, player):
        if self.attacking and self.frame_index>=7 and self.frame_index<11 and not self.dead:
            if self.facing_right:
                if ((player.rect.x+player.rect.width)>=(self.rect.x+104)) and (player.rect.x<=self.rect.x+236) and player.rect.top<=self.rect.bottom-62 and player.rect.bottom>=self.rect.top+122 and not self.has_attacked:
                    player.health-=10
                    self.has_attacked=True
                    # print('a')
            else:
                if ((player.rect.x+player.rect.width)>=(self.rect.x+20)) and (player.rect.x<=self.rect.x+152) and player.rect.top<=self.rect.bottom-62 and player.rect.bottom>=self.rect.top+122 and not self.has_attacked:
                    player.health-=10
                    self.has_attacked=True
                    # print('b')

            if player.health<0:
                player.health=0

        
               
        # print(player.health, self.health)
    def run(self, player):
        self.update(player)
        self.handle_player_collisions(player)
        self.animate()

