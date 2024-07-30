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
        self.shell_thrown=0
        self.shell_kicked=0
        self.shell_stopped=0
        self.thrown_up=0
        self.shell_regrab=0
        self.paused=False
        self.pause_start=0
        self.shift_player=False
        self.dont_shift=False

        self.right_calibration=level_width
        self.left_calibration=0
    
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
        self.shells=pygame.sprite.Group()
        self.falling_platforms=pygame.sprite.Group()
        self.spikes=pygame.sprite.Group()
        self.flames=pygame.sprite.Group()
        self.on_flames=pygame.sprite.Group()
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
                elif cell == 'L':
                    tile=Shell((x, y))
                    self.shells.add(tile)
                    print(len(self.shells))
                elif cell == 'J':
                    tile = Falling_Platform((x, y), tile_size)
                    self.tiles.add(tile)
                    self.falling_platforms.add(tile)
                elif cell == 'Y':
                    tile=Spike((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'U':
                    tile=Firejet((x, y), tile_size)
                    self.tiles.add(tile)
                    flame=Flame((x, y-64), tile_size)
                    self.flames.add(flame)
                    self.on_flames.add(flame)


    def scroll_x(self):
        self.shift_x = 0

        player = self.player.sprite
        
        if player.facing_right:
            if player.coords.x<screen_width/3 or self.right_calibration<screen_width:
                self.shift_x=0
            elif player.pos.x>screen_width/3:
                self.shift_x=-3*(player.prev_x_vel)/2
                player.pos.x-=3*player.prev_x_vel/2
            
            else:
                self.shift_x=-player.prev_x_vel
                player.pos.x-=player.prev_x_vel
        else:
            if self.left_calibration>0 or player.coords.x>level_width-screen_width/3:
                self.shift_x=0
            elif player.pos.x<2*screen_width/3:
                self.shift_x=-3*(player.prev_x_vel)/2
                player.pos.x-=3*player.prev_x_vel/2
            
            else:
                self.shift_x=-player.vel.x
                player.pos.x-=player.vel.x


        # print('cam', player.vel.x, player.prev_x_vel)
        self.right_calibration+=self.shift_x
        self.left_calibration+=self.shift_x

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
        # print('pxcol', player.vel.x)
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

        # print(self.shift_player, self.dont_shift, player.coords.x, player.pos.x)
        player.pos.x+=player.vel.x

        player.coords.x+=player.vel.x

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

        for shell in self.shells.sprites():
            shell.move_x(self.shift_x, player.rect.x, player.coords.x)

        for flame in self.flames.sprites():
            flame.move_x(self.shift_x)

        self.tiles.update(self.shift_x, 0)

        # for p in self.h_moving_platforms:
        #     print('pv', p.vel.x)
        # print('prect' ,player.rect.x+player.rect.width)
        # print('x_sol', player.rect.x+player.rect.width, player.rect.y)
        for tile in self.tiles.sprites():
            # print(tile.rect.x, end=' ')
            if tile.rect.colliderect(player.rect):
                # print('c', end=' ')
                f=1

                # print('cx', tile.rect.top, player.rect.top)
                vel=player.vel.x-tile.vel.x

                if tile.__class__==Bullet:
                    if not tile.bounced_on:
                        # print('cx', tile.rect.x, player.rect.x, tile.rect.y, player.rect.y)
                        player.dead=True
                else:
                    if (tile.__class__==On_Block and self.on==False) or (tile.__class__==Off_Block and self.on==True) or tile.__class__==Falling_Platform:
                        pass
                    else:
                        if vel<0:
                            player.pos.x = tile.rect.right
                            player.touching_wall_l=True
                            player.coords.x = tile.coords.x+tile_size
                            player.rect.x = int(player.pos.x)
                            player.vel.x=0
                            if tile.__class__==Spike:
                                player.dead=True

                        elif vel>0:
                            player.pos.x = tile.rect.left - player.rect.width
                            player.touching_wall_r=True
                            player.rect.x = int(player.pos.x)
                            player.coords.x = tile.coords.x - player.rect.width
                            # print(player.pos.x, player.rect.x)
                            player.vel.x = 0
                            if tile.__class__==Spike:
                                player.dead=True

            for shell in self.shells.sprites(): #shell-tile collision
                if tile.rect.colliderect(shell.rect):
                    if (tile.__class__==On_Block and self.on==False) or (tile.__class__==Off_Block and self.on==True):
                        pass
                    else:
                        if shell.held:
                            pygame.sprite.Sprite.kill(shell)
                            player.holding_shell=False
                        else:
                            vel = shell.vel.x - tile.vel.x
                            if tile.__class__==On_Off_Switch:
                                self.on=not self.on
                            if vel<0:
                                shell.pos.x = tile.rect.right
                                shell.coords.x = tile.coords.x+tile_size
                                shell.rect.x = int(shell.pos.x)
                                shell.vel.x=-shell.vel.x

                            elif vel>0:
                                shell.pos.x = tile.rect.left - shell.rect.width
                                shell.rect.x = int(shell.pos.x)
                                shell.coords.x = tile.coords.x - shell.rect.width
                                shell.vel.x = -shell.vel.x
                        

        #player-shell collisions

        keys=pygame.key.get_pressed()
        
        for shell in self.shells.sprites():
            if shell.rect.colliderect(player.rect) and not player.dead:
                if shell.kicked:
                    t=pygame.time.get_ticks()
                    if(t-self.shell_thrown>100) and (t-self.shell_kicked>100) and (t-self.thrown_up>100) and (t-self.shell_regrab)>100:
                        player.dead=True
                else:
                    if keys[pygame.K_LSHIFT] and not player.holding_shell:
                        shell.held=True
                        player.holding_shell=True
                    else:
                        t=pygame.time.get_ticks()
                        if t-self.thrown_up>100:
                            if player.vel.x>0:
                                shell.vel.x=12
                                shell.kicked=True
                                self.shell_kicked=pygame.time.get_ticks()
                                player.pos.x = shell.rect.left - player.rect.width
                                player.rect.x = int(player.pos.x)
                                player.coords.x = shell.coords.x - player.rect.width
                            elif player.vel.x<0:
                                shell.vel.x=-12
                                shell.kicked=True
                                self.shell_kicked=pygame.time.get_ticks()
                                player.pos.x = shell.rect.right
                                player.coords.x = shell.coords.x+shell.rect.width
                                player.rect.x = int(player.pos.x)
            # print(player.vel.x, shell.vel.x)

        

        
        if player.status=='wall_slide' and f==0:
            if player.touching_wall_l:
                player.touching_wall_l=False
                player.vel.x-=1
            elif player.touching_wall_r:
                player.touching_wall_r=False
                player.vel.x-=1

        if player.stationary_x and f==0:
            if player.touching_wall_l:
                player.touching_wall_l=False
                player.vel.x-=1
            elif player.touching_wall_r:
                player.touching_wall_r=False
                player.vel.x-=1

        # print('xcol', player.vel.x)

    def y_collisions(self):

        keys=pygame.key.get_pressed()

        player = self.player.sprite
        player.acc.y = 1
        if(player.slow_jump):
            player.acc.y=0.45
        if(player.status=='wall_slide'):
            player.acc.y=0.2
        if(player.on_fp):
            player.acc.y=0
        player.vel.y+=player.acc.y
        player.pos.y += player.vel.y
        player.coords.y += player.vel.y
        player.rect.y = int(player.pos.y)


        for b in self.bullets.sprites():
            b.move_y()

        for shell in self.shells.sprites():
            shell.move_y(self.shift_y, player.pos.y-31, player.coords.y-31)

        for flame in self.flames.sprites():
            flame.move_y(self.shift_y)

        for p in self.falling_platforms.sprites():
            p.move()
            self.fp_speed=p.vel.y
            if p.rect.y>level_height:
                pygame.sprite.Sprite.kill(p)

        if player.on_fp:
            player.pos.y+=self.fp_speed+1
            player.coords.y+=self.fp_speed
            player.rect.y=int(player.pos.y)+1

        

        self.tiles.update(0, self.shift_y)

       
        # print(player.vel.y)
        # print('b', player.vel.x, player.rect.x, player.rect.x+player.rect.width)
        # print('y_sol_1', player.rect.y,player.pos.y, player.vel.y)
        
        
        f=0
        for tile in self.tiles.sprites():
            # print(tile.__class__)

            # print(tile.rect.top, end=' ')
            if tile.rect.colliderect(player.rect):

                #falling platforms
                if tile.__class__==Falling_Platform:
                    f=1
                    if player.vel.y>=0:
                        player.pos.y = tile.rect.top - player.rect.height+1
                        player.rect.y = int(player.pos.y)
                        player.coords.y = tile.coords.y - player.rect.height
                        player.vel.y = 0
                        player.on_ground = True
                        player.jumped=False
                        tile.triggered=True
                        player.on_fp=True
                        self.fp_speed=tile.vel.y
                        # print(self.fp_speed)

                if (tile.__class__==On_Block and self.on==False) or (tile.__class__==Off_Block and self.on==True) or tile.__class__==Falling_Platform:
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

                        if tile.__class__==Spike:
                            player.dead=True

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
                            player.vel.y = 0
                            player.on_ground = True
                            player.jumped=False
                            if tile.__class__==Spike:
                                player.dead=True
                            if tile.__class__==H_Moving_Platform:
                                f=1
                                player.on_h_platform=True
                                self.hp_speed=tile.vel.x
                            else:
                                self.hp_speed=0

                    else:
                        if player.on_h_platform:
                            f=1
                        if player.on_fp:
                            player.pos.y = tile.rect.top - player.rect.height
                            player.rect.y = int(player.pos.y)
                            player.coords.y = tile.coords.y - player.rect.height
                            player.vel.y = 0
                            player.on_ground = True
                            player.jumped=False


       

               
            # print(len(self.shells))
            for shell in self.shells.sprites():
                # print(shell.rect.bottom, tile.rect.top)
                if tile.rect.colliderect(shell.rect): #shell-tile collision
                    # print('pls')
                    if (tile.__class__==On_Block and self.on==False) or (tile.__class__==Off_Block and self.on==True):
                        pass
                    else:
                        if shell.held:
                            pygame.sprite.Sprite.kill(shell)
                            player.holding_shell=False
                        else:
                            if shell.vel.y<0:
                                shell.pos.y = tile.rect.bottom 
                                shell.rect.y = int(shell.pos.y)
                                shell.coords.y = tile.coords.y + tile_size
                                shell.vel.y=0
                            elif shell.vel.y>0:
                                shell.pos.y = tile.rect.top - shell.rect.height
                                shell.rect.y = int(shell.pos.y)
                                shell.coords.y = tile.coords.y - shell.rect.height
                                shell.vel.y = 0

        #player-shell collision

        for shell in self.shells.sprites():
            # print(shell.rect.bottom+shell.rect.width, tile.rect.top)
            if shell.rect.colliderect(player.rect) and not shell.held and not player.dead:
                if shell.rect.y>player.rect.y:
                    player.pos.y = shell.rect.top - player.rect.height
                    t=pygame.time.get_ticks()
                    if shell.kicked and t-self.shell_kicked>100:
                        shell.kicked=False
                        if keys[pygame.K_d]:
                            player.vel.y=-15
                        else:
                            player.vel.y=-10
                        shell.vel.x=0
                        player.pos.y-=2
                        player.coords.y-=2
                        player.rect.y=int(player.pos.y)
                        self.shell_stopped=pygame.time.get_ticks()
                        # print('stop', self.shell_stopped)
                    else:
                        t=pygame.time.get_ticks()
                        # print(t, self.shell_stopped)
                        if t-self.shell_stopped>100:
                            if player.rect.centerx<=shell.rect.centerx:
                                shell.vel.x=12
                            else:
                                shell.vel.x=-12
                            shell.kicked=True
                            self.shell_kicked=pygame.time.get_ticks()
                else:
                    if not player.holding_shell:
                        shell.held=True
                        player.holding_shell=True
                        self.shell_regrab=pygame.time.get_ticks()
                        shell.pos.y=player.pos.y-31
                        shell.coords.y=player.coords.y-31
                        shell.rect.y=int(shell.rect.y)
                    # print('regrab')



        if f==0 and player.on_h_platform:
            player.vel.x+=self.hp_speed
            player.on_h_platform=False

        if player.on_fp and f==0:
            player.on_fp=False
                

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

    def handle_shells(self):
        keys=pygame.key.get_pressed()
        player=self.player.sprite
        
        for shell in self.shells.sprites():
            if shell.coords.y>level_height:
                pygame.sprite.Sprite.kill(shell)
            
            if shell.held and not keys[pygame.K_LSHIFT]:
                shell.held=False
                player.holding_shell=False
                if keys[pygame.K_UP]:
                    shell.vel.y=-20
                    shell.vel.x=player.vel.x
                    self.thrown_up=pygame.time.get_ticks()
                    shell.kicked=True
                else:
                    if player.facing_right:
                        shell.vel.x=12
                    else:
                        shell.vel.x=-12
                    shell.vel.y=-5
                    shell.kicked=True
                    self.shell_thrown=pygame.time.get_ticks()

            # print(shell.held, shell.vel, shell.kicked)

    
    def handle_flames(self):
        player=self.player.sprite
        for flame in self.flames.sprites():
            # print(flame.on)
            if self.time%flame.freq==0:
                if flame.on:
                    self.on_flames.remove(flame)
                else:
                    self.on_flames.add(flame)
                flame.on=not flame.on

            if flame.rect.colliderect(player.rect) and flame.on:
                player.dead=True

        # print(len(self.flames), len(self.on_flames))
  

    def run(self):
        player=self.player.sprite

        keys=pygame.key.get_pressed()
        t=pygame.time.get_ticks()
        if keys[pygame.K_RSHIFT] and (t-self.pause_start>500):
            self.paused=not self.paused
            self.pause_start=pygame.time.get_ticks()

         
        for tile in self.on_off_switches.sprites():
            tile.change_sprite(self.on)
        for tile in self.on_blocks.sprites():
            tile.change_sprite(self.on)
        for tile in self.off_blocks.sprites():
            tile.change_sprite(self.on)

        self.tiles.draw(self.display_surface)

        if not self.paused:
            self.shoot_canon()
            self.handle_shells()
            self.handle_flames()

        self.bullets.draw(self.display_surface)
        self.shells.draw(self.display_surface)
        self.on_flames.draw(self.display_surface)
        

        if not self.paused:
            self.player.update()
            self.scroll_x()
            self.x_collisions() 
            
            self.scroll_y()
            self.y_collisions()
        if player.sliding:
            player.rect.y+=25
        self.player.draw(self.display_surface)

        if player.sliding:
                player.rect.y-=25

        if not self.paused:
            self.time+=1

        

               