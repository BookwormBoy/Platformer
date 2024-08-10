import pygame, sys
from settings import *
from level import Level
from game_data import *
from overworld import Overworld
from pygame import mixer
mixer.init()
mixer.music.load('./audio/level.ogg')
mixer.music.play(-1)


class Game():
    def __init__(self):
        self.overworld=Overworld(1, 1, screen, self.create_level)
        self.status='overworld'
    def create_level(self,current_level):
        self.level = Level(level_map,current_level,level_csv[current_level], screen,self.create_overworld)
        self.status = 'level'
        # channel_1.play(sound2, -1)

    def create_overworld(self,current_level,new_max_level):
        self.overworld = Overworld(current_level,new_max_level,screen,self.create_level)
        self.status = 'overworld'
        # channel_1.play(sound1, -1)
    def run(self):
        if self.status=='overworld':
            self.overworld.run()
        elif self.status=='level':
            self.level.run()
        # print(self.status)
pygame.init()
screen=pygame.display.set_mode((screen_width, screen_height))
clock=pygame.time.Clock()
# level = Level(level_map, level_3, screen)
# overworld = Overworld(1, 4, screen)
game=Game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    game.run()

    pygame.display.update()
    clock.tick(60)