import pygame
from tiles import *
from player import Player
from settings import *
from enemies import *
# from main import level_music


class Level:
    def __init__(self, level_data, current_level, level_csv, surface, create_overworld, music1, music2):
        self.display_surface = surface
        self.offset_x=0
        self.offset_y=0
        self.player_start_x=64
        self.player_start_y=500
        self.checkpoint_reached=False
        self.ckpt_x=0
        self.ckpt_y=0
        self.time=0
        self.current_level=current_level
        self.create_overworld=create_overworld
        self.win_music=music1
        self.boss_music=music2
        

        self.setup_level(level_data, level_csv)
        self.shift_x = 0
        self.shift_y = 0
        self.level_data=level_data
        self.level_csv=level_csv

        self.shifted=False
        self.start_ypos=0
        self.hp_speed=0
        self.prev_hp_speed=0
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
        self.level_clear=False
        self.win=False

        self.right_calibration=level_width[self.current_level]+self.offset_x
        self.left_calibration=0+self.offset_x

        self.player_healthbar=pygame.image.load('./graphics/healthbars/healthbar.png')
        self.player_healthbar = pygame.transform.scale(self.player_healthbar, (306, 24))
        self.player_health=pygame.Surface((300, 18))
        self.player_health.fill('red')

        self.ninja_healthbar=pygame.image.load('./graphics/healthbars/healthbar.png')
        self.ninja_healthbar = pygame.transform.scale(self.ninja_healthbar, (306, 24))
        self.ninja_health=pygame.Surface((300, 18))
        self.ninja_health.fill('blue')

        font = pygame.font.Font('Pixeltype.ttf', 92)
        text='You Won!'
        self.wintext = font.render(text, True, 'black')

        
    def create_tile_group(self,layout, sheet, tile_type):
        sprite_group = pygame.sprite.Group()
        if sheet == 'terrain':
            terrain_tile_list = import_cut_graphics('./graphics/terrain/terrain_tiles.png', 16)

        elif sheet == 'caves':
            terrain_tile_list = import_cut_graphics('./graphics/terrain/caves.png', 16)


        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val!= '-1':
                    x=col_index*tile_size+self.offset_x
                    y=row_index*tile_size+self.offset_y
                    
                    if tile_type=='terrain':
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = Tile((x,y), (x-self.offset_x,y-self.offset_y), tile_surface)
                    elif tile_type=='bg':
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = Bg_Tile((x,y), (x-self.offset_x,y-self.offset_y), tile_surface)
                    elif tile_type=='hmp':
                        tile_surface=pygame.image.load('./graphics/terrain/h_moving_platform.png')
                        tile_surface=pygame.transform.scale(tile_surface, (tile_surface.get_size()[0]*1.5, tile_surface.get_size()[1]*1.5))
                        sprite = H_Moving_Platform((x,y), (x-self.offset_x,y-self.offset_y), tile_surface)
                    elif tile_type=='fp':
                        tile_surface=pygame.image.load('./graphics/terrain/falling_platform.png')
                        tile_surface=pygame.transform.scale(tile_surface, (tile_surface.get_size()[0]*1.5, tile_surface.get_size()[1]*1.5))
                        sprite = Falling_Platform((x,y), (x-self.offset_x,y-self.offset_y), tile_surface)
                    elif tile_type=='spikes':
                        tile_surface=pygame.image.load('./graphics/terrain/spike.png')
                        tile_surface=pygame.transform.scale(tile_surface, (tile_surface.get_size()[0]*2, tile_surface.get_size()[1]*2))
                        sprite = Spike((x,y), (x-self.offset_x,y-self.offset_y), tile_surface)
                    elif tile_type=='canon':
                        tile_surface=pygame.image.load('./graphics/terrain/canon.png')
                        sprite = Canon((x,y), (x-self.offset_x,y-self.offset_y), tile_surface)
                    elif tile_type=='switch':
                        tile_surface=pygame.image.load('./graphics/terrain/switch/on.png')
                        sprite = On_Off_Switch((x,y), (x-self.offset_x,y-self.offset_y), tile_surface)
                    elif tile_type=='on_block':
                        tile_surface=pygame.image.load('./graphics/terrain/on_blocks/on_active.png')
                        sprite = On_Block((x,y), (x-self.offset_x,y-self.offset_y), tile_surface)
                    elif tile_type=='off_block':
                        tile_surface=pygame.image.load('./graphics/terrain/off_blocks/off_active.png')
                        sprite = Off_Block((x,y), (x-self.offset_x,y-self.offset_y), tile_surface)
                    elif tile_type=='shell':
                        tile_surface=pygame.image.load('./graphics/terrain/shell.png')
                        sprite = Shell((x,y), (x-self.offset_x,y-self.offset_y), tile_surface)
                    elif tile_type=='firejet':
                        tile_surface=pygame.image.load('./graphics/terrain/flame.png')
                        sprite = Flame((x,y-32), (x-self.offset_x,y-self.offset_y))
                    elif tile_type=='goal':
                        tile_surface=pygame.image.load('./graphics/terrain/goal/tile000.png')
                        sprite = Goal((x,y), (x-self.offset_x,y-self.offset_y), tile_surface)
                    elif tile_type=='ckpt':
                        tile_surface=pygame.image.load('./graphics/terrain/flag/tile000.png')
                        sprite = Checkpoint((x,y), (x-self.offset_x,y-self.offset_y), tile_surface)
                        self.ckpt_x=x-self.offset_x
                        self.ckpt_y=y-self.offset_y
                    sprite_group.add(sprite)

        return sprite_group 
    
    def create_group_single(self, layout, entity):
        sprite_group = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val!= '-1':
                    x=col_index*tile_size
                    y=row_index*tile_size

                    if entity =='player':
                        if not self.checkpoint_reached:
                            p = Player((self.player_start_x, self.player_start_y), (x, y))
                            self.offset_x = self.player_start_x - x
                            if not self.current_level==4:
                                self.offset_y = self.player_start_y - y
                        else:
                            p = Player((self.player_start_x, self.player_start_y), (self.ckpt_x , self.ckpt_y))

                        sprite_group.add(p)

                    elif entity == 'ninja':
                        nin = Ninja((x, y))
                        sprite_group.add(nin)
                        
        return sprite_group

                        
       
    
    def setup_level(self, layout, level_csv ):
        self.time=250
        self.on=True
        self.right_calibration=level_width[self.current_level]+self.offset_x
        self.left_calibration=0+self.offset_x
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
        self.checkpoints=pygame.sprite.Group()
        self.ninja=pygame.sprite.GroupSingle()
        self.falling_spikes=pygame.sprite.Group()
        for row_index,row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x=tile_size*col_index+self.offset_x
                y=tile_size*row_index+self.offset_y
                if cell == 'X':
                    tile=Tile((x, y),(x-self.offset_x, y-self.offset_y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'P':
                    p = Player((x-self.offset_x, y-self.offset_y), (x-2*self.offset_x, y-2*self.offset_y))
                    self.player.add(p)
                    self.player_start_x=x-self.offset_x
                    self.player_start_y=y-self.offset_y
                elif cell == 'H':
                    p=H_Moving_Platform((x, y),(x-self.offset_x, y-self.offset_y),  tile_size)
                    self.tiles.add(p)
                    self.h_moving_platforms.add(p)
                elif cell == 'C':
                    c=Canon((x, y), (x-self.offset_x, y-self.offset_y), tile_size)
                    self.tiles.add(c)
                    self.canons.add(c)
                elif cell == 'S':
                    tile=On_Off_Switch((x, y), (x-self.offset_x, y-self.offset_y), tile_size)
                    self.tiles.add(tile)
                    self.on_off_switches.add(tile)
                elif cell == 'N':
                    tile=On_Block((x, y), (x-self.offset_x, y-self.offset_y), tile_size)
                    self.tiles.add(tile)
                    self.on_blocks.add(tile)
                elif cell == 'F':
                    tile=Off_Block((x, y), (x-self.offset_x, y-self.offset_y), tile_size)
                    self.tiles.add(tile)
                    self.off_blocks.add(tile)
                elif cell == 'L':
                    tile=Shell((x, y),(x-self.offset_x, y-self.offset_y))
                    self.shells.add(tile)
                elif cell == 'J':
                    tile = Falling_Platform((x, y), (x-self.offset_x, y-self.offset_y), tile_size)
                    self.tiles.add(tile)
                    self.falling_platforms.add(tile)
                elif cell == 'Y':
                    tile=Spike((x, y), (x-self.offset_x, y-self.offset_y), tile_size)
                    self.tiles.add(tile)
                elif cell == 'U':
                    tile=Firejet((x, y), (x-self.offset_x, y-self.offset_y), tile_size)
                    self.tiles.add(tile)
                    flame=Flame((x, y-64), (x-self.offset_x, y-self.offset_y), tile_size)
                    self.flames.add(flame)
                    self.on_flames.add(flame)
                elif cell == 'K':
                    tile=Checkpoint((x, y), (x-self.offset_x, y-self.offset_y), tile_size)
                    self.checkpoints.add(tile)
                elif cell == 'I':
                    ninja=Ninja((x, y-128))
                    self.ninja.add(ninja)

        player_layout = import_csv_layout(level_csv['player'])
        self.player = self.create_group_single(player_layout, 'player')

        if self.current_level!=4:

            terrain_layout = import_csv_layout(level_csv['terrain'])
            self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain', 'terrain')
            for t in self.terrain_sprites.sprites():
                self.tiles.add(t)

            bg_layout = import_csv_layout(level_csv['bg'])
            self.bg_sprites = self.create_tile_group(bg_layout, 'terrain', 'bg')
            self.tiles.add(self.bg_sprites)

            hmp_layout = import_csv_layout(level_csv['h_moving_platforms'])
            self.h_moving_platforms=self.create_tile_group(hmp_layout, 'hmp', 'hmp')
            self.tiles.add(self.h_moving_platforms)

            falling_platform_layout = import_csv_layout(level_csv['falling_platforms'])
            self.falling_platforms = self.create_tile_group(falling_platform_layout, 'fp', 'fp')
            self.tiles.add(self.falling_platforms)

            falling_platform_layout = import_csv_layout(level_csv['spikes'])
            self.spikes = self.create_tile_group(falling_platform_layout, 'spikes', 'spikes')
            self.tiles.add(self.spikes)

            canon_layout = import_csv_layout(level_csv['canons'])
            self.canons = self.create_tile_group(canon_layout, 'canon', 'canon')
            self.tiles.add(self.canons)

            switch_layout = import_csv_layout(level_csv['switch'])
            self.on_off_switches = self.create_tile_group(switch_layout, 'switch', 'switch')
            self.tiles.add(self.on_off_switches)

            on_blocks_layout = import_csv_layout(level_csv['on_block'])
            self.on_blocks = self.create_tile_group(on_blocks_layout, 'on_block', 'on_block')
            self.tiles.add(self.on_blocks)

            off_blocks_layout = import_csv_layout(level_csv['off_block'])
            self.off_blocks = self.create_tile_group(off_blocks_layout, 'off_block', 'off_block')
            self.tiles.add(self.off_blocks)

            shell_layout = import_csv_layout(level_csv['shell'])
            self.shells = self.create_tile_group(shell_layout, 'shell', 'shell')

            flame_layout = import_csv_layout(level_csv['firejet'])
            self.on_flames = self.create_tile_group(flame_layout, 'firejet', 'firejet')
            # self.flames=pygame.sprite.Group()
            self.flames.add(self.on_flames)

            goal_layout = import_csv_layout(level_csv['goal'])
            self.goal = self.create_tile_group(goal_layout, 'goal', 'goal')
            self.tiles.add(self.goal)


            checkpoint_layout = import_csv_layout(level_csv['checkpoint'])
            self.checkpoints = self.create_tile_group(checkpoint_layout, 'ckpt', 'ckpt')

            self.background=pygame.sprite.Group()
            surface=pygame.image.load('./graphics/terrain/backdrop.png')
            sprite=Bg_Tile((0, 0), (0, 0), surface)
            self.background.add(sprite)

        else:
            terrain_layout = import_csv_layout(level_csv['terrain'])
            self.terrain_sprites = self.create_tile_group(terrain_layout, 'caves', 'terrain')
            for t in self.terrain_sprites.sprites():
                self.tiles.add(t)

            self.background=pygame.sprite.Group()
            surface=pygame.image.load('./graphics/terrain/boss_bg.png')
            sprite=Bg_Tile((0, 0), (0, 0), surface)
            self.background.add(sprite)

            self.goal=pygame.sprite.Group()

            ninja_layout=import_csv_layout(level_csv['ninja'])
            self.ninja = self.create_group_single(ninja_layout, 'ninja')


        

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
            if self.left_calibration>0 or player.coords.x>level_width[self.current_level]-screen_width/3:
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
        if player.on_fp:
            vel=self.fp_speed
        else:
            vel=player.vel.y

        if player.pos.y<screen_height/3 and vel<0 and player.coords.y>screen_height/3:
            self.shift_y = -vel
            player.pos.y += self.shift_y
            if not self.shifted:
                self.start_ypos = player.coords.y
            self.shifted=True
        elif player.pos.y > 2*screen_height/3 and vel>0 and player.coords.y<level_height-screen_width/3:
            self.shift_y = -vel 
            player.pos.y += self.shift_y
            self.shifted=True
        else:
            if(vel<0):
                if(self.shifted and ((not player.on_ground) and (player.coords.y<self.start_ypos))):
                    self.shift_y = -vel
                    player.pos.y += self.shift_y
                else:
                    self.shift_y=0
                    self.shifted=False
            else:
                if(self.shifted and ((not player.on_ground) and (player.coords.y>self.start_ypos))):
                    self.shift_y = -vel
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
            p.move(self.time)

        for b in self.bullets.sprites(): #bullets
            b.move_x()
            if b.coords.x < 0 or b.coords.x>level_width[self.current_level] or b.coords.y<0 or b.coords.y>level_height:
                pygame.sprite.Sprite.kill(b)

        for shell in self.shells.sprites():
            shell.move_x(self.shift_x, player.rect.x, player.coords.x)

        for flame in self.flames.sprites():
            flame.move_x(self.shift_x)

        for c in self.checkpoints.sprites():
            c.move_x(self.shift_x)

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
                    if (tile.__class__==On_Block and self.on==False) or (tile.__class__==Off_Block and self.on==True) or tile.__class__==Falling_Platform or tile.__class__==Bg_Tile or tile.__class__==Goal:
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
                        
            for b in self.bullets.sprites():
                if tile.rect.colliderect(b.rect):
                    if (tile.__class__==On_Block and self.on==False) or (tile.__class__==Off_Block and self.on==True) or tile.__class__==Canon or tile.__class__==Bullet:
                        pass
                    else:
                        # print(tile.__class__)
                        pygame.sprite.Sprite.kill(b)
                        pass

        #player-shell collisions

        keys=pygame.key.get_pressed()
        
        for shell in self.shells.sprites():
            if shell.rect.colliderect(player.rect) and not player.dead:
                if shell.kicked:
                    t=pygame.time.get_ticks()
                    if(t-self.shell_thrown>150) and (t-self.shell_kicked>150) and (t-self.thrown_up>150) and (t-self.shell_regrab)>150:
                        player.dead=True
                else:
                    if keys[pygame.K_LSHIFT] and not player.holding_shell:
                        shell.held=True
                        player.holding_shell=True
                    else:
                        t=pygame.time.get_ticks()
                        if t-self.thrown_up>100:
                            if player.vel.x>0:
                                shell.vel.x=10
                                shell.kicked=True
                                self.shell_kicked=pygame.time.get_ticks()
                                player.pos.x = shell.rect.left - player.rect.width
                                player.rect.x = int(player.pos.x)
                                player.coords.x = shell.coords.x - player.rect.width
                            elif player.vel.x<0:
                                shell.vel.x=-10
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
            shell.move_y(self.shift_y, player.pos.y-35, player.coords.y-35)

        for flame in self.flames.sprites():
            flame.move_y(self.shift_y)

        for c in self.checkpoints.sprites():
            c.move_y(self.shift_y)

        for p in self.falling_platforms.sprites():
            p.move()
            # self.fp_speed=p.vel.y
            if p.rect.y>level_height:
                pygame.sprite.Sprite.kill(p)

        if player.on_fp:
            player.pos.y+=self.fp_speed+1
            player.coords.y+=self.fp_speed+1
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
                        player.coords.y = tile.coords.y - player.rect.height+1
                        player.vel.y = 0
                        player.on_ground = True
                        player.jumped=False
                        tile.triggered=True
                        player.on_fp=True
                        self.fp_speed=tile.vel.y
                        # print(self.fp_speed)

                if (tile.__class__==On_Block and self.on==False) or (tile.__class__==Off_Block and self.on==True) or tile.__class__==Falling_Platform or tile.__class__==Bg_Tile or tile.__class__==Goal:
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
                                if tile.__class__==On_Off_Switch:
                                    self.on=not self.on
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
                            player.vel.y=-19
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
                                shell.vel.x=10
                            else:
                                shell.vel.x=-10
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
            self.fp_speed=0
                

        # print('ycol', player.vel)


        if player.on_ground and (player.vel.y>1 or player.vel.y<0):
            player.on_ground = False

        # print('og',player.on_ground)

        # print()
        
        

        # print('y_col', player.pos.y, player.rect.y)


        # print(player.rect.y, player.pos.y)
            
        


    def shoot_canon(self):
        for canon in self.canons:
            if self.time%canon.freq==0:
                bullet_surface=pygame.image.load('./graphics/terrain/bullet.png')
                bullet_surface=pygame.transform.scale(bullet_surface, (32, 32))
                bullet=Bullet((canon.rect.x, canon.rect.y-10),(canon.rect.x-self.offset_x, canon.rect.y-10-self.offset_y), bullet_surface)
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

    def handle_checkpoints(self):
        player=self.player.sprite
        for c in self.checkpoints.sprites():
            if c.rect.colliderect(player.rect):
                self.player_start_x = 640
                self.player_start_y= 500
                self.offset_x= self.player_start_x-c.coords.x
                self.offset_y = self.player_start_y - c.coords.y
                self.checkpoint_reached=True

        # print(self.offset_x, self.offset_y)

    def handle_falling_spikes(self):
        player=self.player.sprite
        if self.time%300==0:
            fs=Falling_Spike((player.rect.x, 0), 64)
            self.falling_spikes.add(fs)

        for fs in self.falling_spikes.sprites():
            fs.update()
            if fs.rect.colliderect(player.rect):
                player.health-=10
                pygame.sprite.Sprite.kill(fs)

            for tile in self.tiles.sprites():
                if fs.rect.colliderect(tile.rect):
                    pygame.sprite.Sprite.kill(fs)

    def handle_goal(self):
        player=self.player.sprite
        for g in self.goal.sprites():
            if g.rect.colliderect(player.rect):
                self.level_clear=True



        

    def reset(self):
        self.setup_level(self.level_data, self.level_csv)
  

    def run(self):
        player=self.player.sprite
        ninja=self.ninja.sprite

        keys=pygame.key.get_pressed()
        t=pygame.time.get_ticks()
        if keys[pygame.K_RSHIFT] and (t-self.pause_start>300):
            self.paused=not self.paused
            self.pause_start=pygame.time.get_ticks()

         
        for tile in self.on_off_switches.sprites():
            tile.change_sprite(self.on)
        for tile in self.on_blocks.sprites():
            tile.change_sprite(self.on)
        for tile in self.off_blocks.sprites():
            tile.change_sprite(self.on)

        self.background.draw(self.display_surface)
        self.tiles.draw(self.display_surface)

        if not self.current_level==4:
            self.bg_sprites.draw(self.display_surface)

        if not self.paused:
            self.shoot_canon()
            self.handle_shells()
            self.handle_flames()
            self.handle_checkpoints()
            self.handle_goal()
            if self.current_level==4 and not self.win:
                self.handle_falling_spikes()
            if len(self.ninja)==1:
                ninja.run(player)

        if not self.current_level==4:
            self.bullets.draw(self.display_surface)
            self.shells.draw(self.display_surface)
            self.on_flames.draw(self.display_surface)
            self.checkpoints.draw(self.display_surface)
        else:
            if not self.win:
                self.falling_spikes.draw(self.display_surface)
        if len(self.ninja)==1:
            self.ninja.draw(self.display_surface)

        if not self.paused:
            self.player.update(ninja)
            if not self.current_level==4:
                self.scroll_x()
            self.x_collisions() 
            if not self.current_level==4:
                self.scroll_y()
            self.y_collisions()
        # print(player.coords.y)

        if self.current_level==4:
            # print('ho')
            self.display_surface.blit(self.player_healthbar, (30, 50))
            self.player_health=pygame.Surface((player.health*3, 15))
            self.player_health.fill('#b51d57')
            self.display_surface.blit(self.player_health, (33, 53))

            self.display_surface.blit(self.ninja_healthbar, (1280-330, 50))
            self.ninja_health=pygame.Surface((ninja.health*3, 15))
            self.ninja_health.fill('#295eb3')
            self.display_surface.blit(self.ninja_health, (1280-327+(300-ninja.health*3), 53))

            player.effects.draw(self.display_surface)
            ninja.effects.draw(self.display_surface)

        # if player.attacking:
        #     player.rect.y-=12
        if player.sliding:
            player.rect.y+=25
        self.player.draw(self.display_surface)
        # if player.attacking:
        #     player.rect.y+=12
        if player.sliding:
            player.rect.y-=25

        if not self.paused:
            self.time+=1

        if self.current_level==4 and ninja.health==0:
            if not self.win:
                self.boss_music.stop()
                self.win_music.play(-1)
            self.win=True
            


        if (player.dead and player.frame_index>=6 )or player.coords.y+player.rect.height>level_height:
            self.reset()        

        if self.level_clear:
            self.create_overworld(self.current_level, self.current_level+1)
            # mixer.quit()

        if self.win:
            pygame.Surface.blit(self.display_surface, self.wintext, (500,430))

               