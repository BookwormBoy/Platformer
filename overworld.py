import pygame
from player import Player
from level import Level
from settings import *
from game_data import *
from tiles import Bg_Tile
from support import import_csv_layout

class Overworld():
    def __init__(self, current_level, max_level, surface, create_level):
        self.current_level=current_level
        self.max_level=max_level
        self.player=pygame.sprite.GroupSingle() 
        self.level_selected=current_level
        self.level_pos={1:300, 2:500, 3:700, 4:999}
        self.player_moving=False
        self.target_level=0
        p=Player((self.level_pos[current_level], 400), (0, 0))
        self.player.add(p)
        self.display_surface=surface
        self.status=0
        self.create_level=create_level
        self.setup()
        overworld_layout=import_csv_layout('./levels/overworld/overworld.csv')
        self.setup_csv(overworld_layout)

    def setup(self):
        self.bg=pygame.sprite.Group()
        self.grass=pygame.sprite.Group()
        self.trees=pygame.sprite.Group()
        self.ground=pygame.sprite.Group()
        self.sky=pygame.sprite.Group()

        for i in range(1, 5):
            stage_surface = pygame.image.load('./graphics/terrain/stage.png')
            stage=Bg_Tile((self.level_pos[i]-27, 418), (0,0), stage_surface)
            self.bg.add(stage)

        for i in range(1, 3):
            if i<self.max_level:
                surface = pygame.image.load('./graphics/terrain/path1.png')
                sprite=Bg_Tile((self.level_pos[i]+67, 445), (0,0), surface)
                self.bg.add(sprite)

        if self.max_level==4:
            surface=pygame.image.load('./graphics/terrain/path.png')
            sprite=Bg_Tile((765, 445), (0,0), surface)
            self.bg.add(sprite)

            surface=pygame.image.load('./graphics/terrain/path2.png')
            sprite=Bg_Tile((765+127, 445), (0,0), surface)
            self.bg.add(sprite)

        for i in range(0, 10):
            for j in range(0, 7):
                surface=pygame.image.load('./graphics/terrain/grass.png')
                sprite=Bg_Tile((128*i, 128*j), (0, 0), surface)
                self.grass.add(sprite)

        surface=pygame.image.load('./graphics/terrain/statue.png')
        sprite=Bg_Tile((600, 200), (0, 0), surface)
        self.bg.add(sprite)

    def setup_csv(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val!= '-1':
                    x=col_index*16
                    y=row_index*16
                    if val=='0':
                        surface=pygame.image.load('./graphics/terrain/Green-Tree.png')
                        sprite=Bg_Tile((x+85, y-200), (0, 0), surface)
                        self.trees.add(sprite)
                        
                    elif val=='1':
                        surface=pygame.image.load('./graphics/terrain/pillar.png')
                        sprite=Bg_Tile((x, y), (0, 0), surface)
                        self.bg.add(sprite)

                    elif val=='2':
                        surface=pygame.image.load('./graphics/terrain/bush.png')
                        sprite=Bg_Tile((x, y), (0, 0), surface)
                        self.bg.add(sprite)

                    elif val=='3':
                        surface=pygame.Surface((16, 16))
                        surface.fill('#806724')
                        sprite=Bg_Tile((x, y), (0, 0), surface)
                        self.ground.add(sprite)

                    elif val=='4':
                        surface=pygame.Surface((16, 16))
                        surface.fill('#b2bef7')
                        sprite=Bg_Tile((x, y), (0, 0), surface)
                        self.sky.add(sprite)

                    
                        


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
        self.grass.draw(self.display_surface)
        self.sky.draw(self.display_surface)
        self.ground.draw(self.display_surface)
        self.bg.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.trees.draw(self.display_surface)

        

            

    