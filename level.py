import pygame
from tiles import *
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
        self.hp_speed=0
        self.prev_hp_speed=0
        self.time=0
        self.on=True
    
    def setup_level(self, layout ):
        self.tiles = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.ropes = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemy = pygame.sprite.GroupSingle()
        self.h_moving_platforms=pygame.sprite.Group()
        self.canons=pygame.sprite.Group()
        self.bullets=pygame.sprite.Group()
        self.on_off_switches=pygame.sprite.Group()
        self.on_blocks=pygame.sprite.Group()
        self.off_blocks=pygame.sprite.Group()
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
                elif cell == 'H':
                    p=H_Moving_Platform((x, y), tile_size)
                    self.tiles.add(p)
                    self.h_moving_platforms.add(p)
                elif cell == 'C':
                    c=Canon((x, y), tile_size)
                    self.tiles.add(c)
                    self.canons.add(c)
                elif cell == 'S':
                    tile=On_Off_Switch((x, y), tile_size)
                    self.tiles.add(tile)
                    self.on_off_switches.add(tile)
                elif cell == 'N':
                    tile=On_Block((x, y), tile_size)
                    self.tiles.add(tile)
                    self.on_blocks.add(tile)
                elif cell == 'F':
                    tile=Off_Block((x, y), tile_size)
                    self.tiles.add(tile)
                    self.off_blocks.add(tile)


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

       

        # print(player.coords.x, player.pos.x, self.shift_x)

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
        # print('pxcol', player.vel.x, end=' ')
        # print(player.on_h_platform)
        # if player.on_h_platform:
        #     print(player.vel.x, self.hp_speed, self.prev_hp_speed)

        #     player.vel.x-=self.prev_hp_speed
        #     player.vel.x+=self.hp_speed
        #     print('a', player.vel.x)
        #     self.prev_hp_speed=self.hp_speed

        player.vel.x+=player.acc.x
        if(player.vel.x>player.runspeed):
            player.vel.x=player.runspeed
        if(player.vel.x<-player.runspeed):
            player.vel.x=-player.runspeed
        
        f=0
        if player.status=='wall_slide' or player.vel.x==0:
            if player.touching_wall_r:
                player.vel.x+=1
            elif player.touching_wall_l:
                player.vel.x-=1

        player.pos.x += player.vel.x
        player.coords.x += player.vel.x

        if player.on_h_platform:
            player.pos.x+=self.hp_speed
            player.coords.x+=self.hp_speed
        player.rect.x = int(player.pos.x)

        for p in self.h_moving_platforms: #horizontal moving platforms
            p.move()

        for b in self.bullets.sprites(): #bullets
            b.move_x()
            if b.coords.x < 0 or b.coords.x>level_width or b.coords.y<0 or b.coords.y>level_height:
                pygame.sprite.Sprite.kill(b)

        self.tiles.update(self.shift_x, 0)

        # for p in self.h_moving_platforms:
        #     print('pv', p.vel.x)
        
        # print('x_sol', player.rect.x+player.rect.width, player.rect.y)
        for tile in self.tiles.sprites():
            # print(tile.rect.top, end=' ')
            if tile.rect.colliderect(player.rect):
                f=1

                # print('cx', tile.rect.top, player.rect.top)
                vel=player.vel.x-tile.vel.x

                if tile.__class__==Bullet:
                    if not tile.bounced_on:
                        print('cx', tile.rect.x, player.rect.x, tile.rect.y, player.rect.y)
                        player.dead=True
                else:
                    if (tile.__class__==On_Block and self.on==False) or (tile.__class__==Off_Block and self.on==True):
                        pass
                    else:
                        if vel<0:
                            player.pos.x = tile.rect.right
                            player.touching_wall_l=True
                            player.coords.x = tile.coords.x+tile_size
                            player.rect.x = int(player.pos.x)
                            player.vel.x=0

                        elif vel>0:
                            player.pos.x = tile.rect.left - player.rect.width
                            player.touching_wall_r=True
                            player.rect.x = int(player.pos.x)
                            player.coords.x = tile.coords.x - player.rect.width
                            # print(player.pos.x, player.rect.x)
                            player.vel.x = 0

        
        if player.status=='wall_slide' and f==0:
            if player.touching_wall_l:
                player.touching_wall_l=False
            elif player.touching_wall_r:
                player.touching_wall_r=False

        if player.stationary_x and f==0:
            if player.touching_wall_l:
                player.touching_wall_l=False
            elif player.touching_wall_r:
                player.touching_wall_r=False

        # print('xcol', player.vel.x, end=' ')

    def y_collisions(self):

        keys=pygame.key.get_pressed()

        player = self.player.sprite
        player.acc.y = 1
        if(player.slow_jump):
            player.acc.y=0.45
        if(player.status=='wall_slide'):
            player.acc.y=0.2
        player.vel.y+=player.acc.y
        player.pos.y += player.vel.y
        player.coords.y += player.vel.y
        player.rect.y = int(player.pos.y)

        for b in self.bullets.sprites():
            b.move_y()

        self.tiles.update(0, self.shift_y)
       
        # print(player.vel.y)
        # print('b', player.vel.x, player.rect.x, player.rect.x+player.rect.width)
        # print('y_sol_1', player.rect.y,player.pos.y, player.vel.y)
        
        
        f=0
        for tile in self.tiles.sprites():
            # print(tile.__class__)

            # print(tile.rect.top, end=' ')
            if tile.rect.colliderect(player.rect):

                if (tile.__class__==On_Block and self.on==False) or (tile.__class__==Off_Block and self.on==True):
                        pass
                # print('c')
                else:
                    if player.vel.y<0:
                        player.pos.y = tile.rect.bottom 
                        player.rect.y = int(player.pos.y)
                        player.coords.y = tile.coords.y + tile_size
                        # print(player.rect.y, player.pos.y, tile.rect.bottom)
                        player.vel.y=0
                        if tile.__class__==Bullet and not tile.bounced_on:
                            player.dead=True
                        
                        if tile.__class__==On_Off_Switch:
                            self.on= not self.on

                    elif player.vel.y>0:
                        if tile.__class__==Bullet:
                            if not tile.bounced_on:
                                player.pos.y = tile.rect.top - player.rect.height
                                tile.bounced_on=True
                                if keys[pygame.K_d]:
                                    player.vel.y=-15
                                else:
                                    player.vel.y=-10
                        else:
                            player.pos.y = tile.rect.top - player.rect.height
                            player.rect.y = int(player.pos.y)
                            player.coords.y = tile.coords.y - player.rect.height
                            # print('after c', player.rect.y, tile.rect.top)
                            player.vel.y = 0
                            player.on_ground = True
                            player.jumped=False
                            if tile.__class__==H_Moving_Platform:
                                f=1
                                player.on_h_platform=True
                                self.hp_speed=tile.vel.x
                            else:
                                self.hp_speed=0

                    else:
                        if player.on_h_platform:
                            f=1

        if f==0 and player.on_h_platform:
            player.vel.x+=self.hp_speed
            player.on_h_platform=False

        # print('ycol', player.vel)


        if player.on_ground and (player.vel.y>1 or player.vel.y<0):
            player.on_ground = False

        # print('og',player.on_ground)

        # print()
        
        

        # print('y_col', player.pos.y, player.rect.y)


        # print(player.rect.y, player.pos.y)
            
        # print(self.on)
        


    def shoot_canon(self):
        for canon in self.canons:
            if self.time%canon.freq==0:
                bullet=Bullet((canon.rect.x, canon.rect.y-10), 30)
                self.bullets.add(bullet)
                self.tiles.add(bullet)

  

    def run(self):
        player=self.player.sprite

         
        
        
        
        
        # print(self.shift_x, player.vel.x)
        for tile in self.on_off_switches.sprites():
            tile.change_sprite(self.on)
        for tile in self.on_blocks.sprites():
            tile.change_sprite(self.on)
        for tile in self.off_blocks.sprites():
            tile.change_sprite(self.on)
        # self.tiles.update(self.shift_x, self.shift_y)
        self.tiles.draw(self.display_surface)

        self.shoot_canon()
        # self.handle_bullets()
        # self.bullets.update()
        self.bullets.draw(self.display_surface)

        self.player.update()
        self.scroll_x()
        self.x_collisions() 
        self.scroll_y()
        self.y_collisions()
        # print(player.coords, player.pos, player.vel)
        # print('a', player.vel)
        if player.sliding:
            player.rect.y+=25
        self.player.draw(self.display_surface)
        if player.sliding:
            player.rect.y-=25

        self.time+=1

        

               