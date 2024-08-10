import pygame
from player import Player
from level import Level
from settings import *
from game_data import *

class Overworld():
    def __init__(self, current_level, max_level, surface, create_level):
        self.current_level=current_level
        self.max_level=max_level
        self.player=pygame.sprite.GroupSingle() 
        self.level_selected=current_level
        self.level_pos={1:300, 2:500, 3:700, 4:1000}
        self.player_moving=False
        self.target_level=0
        p=Player((self.level_pos[current_level], 400), (0, 0))
        self.player.add(p)
        self.display_surface=surface
        self.status=0
        self.create_level=create_level

    def move_player(self):
        keys=pygame.key.get_pressed()
        player=self.player.sprite

        if not self.player_moving:
            if keys[pygame.K_RIGHT] and self.level_selected<self.max_level:
                self.target_level=self.level_selected+1
                self.player_moving=True
                player.vel.x=5
                player.status='walk'
                player.facing_right=True
            elif keys[pygame.K_LEFT] and self.level_selected>1:
                self.target_level=self.level_selected-1
                self.player_moving=True
                player.vel.x=-5
                player.status='walk'
                player.facing_right=False
            elif keys[pygame.K_UP]:
                print('h')
                self.create_level(self.level_selected)


        else:
            if abs(player.rect.x - self.level_pos[self.target_level])<6:
                player.rect.x=self.level_pos[self.target_level]
                player.vel.x=0
                player.status='idle'
                self.player_moving=False
                self.level_selected=self.target_level

        player.rect.x+=player.vel.x

    def run(self):
        player=self.player.sprite
        self.move_player()
        player.animate()
        self.player.draw(self.display_surface)

        

            

    