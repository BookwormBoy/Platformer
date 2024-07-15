import pygame
from tiles import Tile
from player import Player
from settings import *

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.shift_x = 0
        self.shift_y = 0
        self.level_data=level_data

        self.shifted=False
        self.start_ypos=0
    
    def setup_level(self, layout ):
        self.tiles = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.ropes = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemy = pygame.sprite.GroupSingle()
        for row_index,row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x=tile_size*col_index
                y=tile_size*row_index
                if cell == 'X':
                    tile=Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'P':
                    p = Player((x, y))
                    self.player.add(p)

    def scroll_x(self):
        self.shift_x = 0

        player = self.player.sprite
        player_x = player.rect.centerx

        if player_x < screen_width/3 and player.vel.x<0 and player.coords.x>screen_width/3:
            self.shift_x = -player.vel.x
            player.pos.x += self.shift_x
        elif player_x > 2*screen_width/3 and player.vel.x>0 and player.coords.x<level_width-screen_width/3:
            self.shift_x = -player.vel.x 
            player.pos.x += self.shift_x
        else:
            self.shift_x = 0

       

        print(player.coords.x, player.pos.x, self.shift_x)

    def scroll_y(self):
        self.shift_y=0

        player = self.player.sprite

        if player.pos.y<screen_height/3 and player.vel.y<0 and player.coords.y>screen_height/3:
            self.shift_y = -player.vel.y
            player.pos.y += self.shift_y
            if not self.shifted:
                self.start_ypos = player.coords.y
            self.shifted=True
        elif player.pos.y > 2*screen_height/3 and player.vel.y>0 and player.coords.y<level_height-screen_width/3:
            self.shift_y = -player.vel.y 
            player.pos.y += self.shift_y
            self.shifted=True
        else:
            if(player.vel.y<0):
                if(self.shifted and ((not player.on_ground) and (player.coords.y<self.start_ypos))):
                    self.shift_y = -player.vel.y
                    player.pos.y += self.shift_y
                else:
                    self.shift_y=0
                    self.shifted=False
            else:
                if(self.shifted and ((not player.on_ground) and (player.coords.y>self.start_ypos))):
                    self.shift_y = -player.vel.y
                    player.pos.y += self.shift_y
                else:
                    self.shift_y=0
                    self.shifted=False

        # print('y_scroll', self.shift_y, player.vel.y, player.pos.y, player.rect.y)
        # print(self.shift_y, player.vel.y, player.pos.y, player.rect.y)
        # print(self.start_ypos)

    def x_collisions(self):

        player = self.player.sprite
        player.vel.x+=player.acc.x
        if(player.vel.x>3):
            player.vel.x=3
        if(player.vel.x<-3):
            player.vel.x=-3
        player.pos.x += player.vel.x
        player.coords.x += player.vel.x
        player.rect.x = int(player.pos.x)
        self.tiles.update(self.shift_x, 0)
        # print('x_col', player.pos.y, player.rect.y)
        for tile in self.tiles.sprites():
            # print(tile.rect.top, end=' ')
            if tile.rect.colliderect(player.rect):
                # print('c')
                # print('cx', tile.rect.top, player.rect.top)
                if player.vel.x<0:
                    player.pos.x = tile.rect.right
                    player.coords.x = tile.coords.x+tile_size
                    player.rect.x = int(player.pos.x)
                    player.vel.x=0

                elif player.vel.x>0:
                    player.pos.x = tile.rect.left - player.rect.width
                    player.rect.x = int(player.pos.x)
                    player.coords.x = tile.coords.x - player.rect.width
                    # print(player.pos.x, player.rect.x)
                    player.vel.x = 0
        
        # print()
    def y_collisions(self):

        player = self.player.sprite
        player.acc.y = 0.6
        if(player.slow_jump):
            player.acc.y=0.45
        player.vel.y+=player.acc.y
        player.pos.y += player.vel.y
        player.coords.y += player.vel.y
        player.rect.y = int(player.pos.y)
        self.tiles.update(0, self.shift_y)
        # print(player.vel.y)
        # print('b', player.vel.x, player.rect.x)
        # print('y_col_1', player.pos.y, player.rect.y)
        f=0
        for tile in self.tiles.sprites():
            # print(tile.rect.top, end=' ')
            if tile.rect.colliderect(player.rect):
                f=1
                # print()
                # print('c')
                if player.vel.y<0:
                    player.pos.y = tile.rect.bottom 
                    player.rect.y = int(player.pos.y)
                    player.coords.y = tile.coords.y + tile_size
                    # print(player.rect.y, player.pos.y, tile.rect.bottom)
                    player.vel.y=0

                elif player.vel.y>0:
                    player.pos.y = tile.rect.top - player.rect.height
                    player.rect.y = int(player.pos.y)
                    player.coords.y = tile.coords.y - player.rect.height
                    # print(player.rect.y, player.pos.y, tile.rect.top)
                    player.vel.y = 0
                    player.on_ground = True
                    player.jumped=False


        if player.on_ground and player.vel.y!=0:
            player.on_ground = False

        # print()
        
        

        # print('y_col', player.pos.y, player.rect.y)


        # print(player.rect.y, player.pos.y)
        


        

    def run(self):
        player=self.player.sprite

         
        
        
        
        
        
        # print(self.shift_x, player.vel.x)
        
        # self.tiles.update(self.shift_x, self.shift_y)
        self.tiles.draw(self.display_surface)

        self.player.update()
        self.scroll_x()
        self.x_collisions() 
        self.scroll_y()
        self.y_collisions()
        # print(player.coords, player.pos, player.vel)
        # print('a', player.vel)
        self.player.draw(self.display_surface)

        

               