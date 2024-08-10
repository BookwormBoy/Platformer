import pygame
from support import import_folder

class Effect(pygame.sprite.Sprite):
    def __init__(self, pos, flip, path):
        super().__init__()
        self.image=pygame.image.load(path)
        self.rect=self.image.get_rect(topleft=pos)
        self.frame_index=0
        self.animation_speed=0.3
        self.done=False
        self.flip=flip

    def animate(self):
        self.frame_index+=self.animation_speed
        if self.frame_index >= len(self.animation):
            self.done=True
            self.frame_index=0

        image=self.animation[int(self.frame_index)]
        if self.flip:
            self.image=pygame.transform.flip(image, True, False)
        else:
            self.image=image

class Blood(Effect):
    def __init__(self, pos, flip):
        super().__init__(pos, flip, './graphics/blood/tile000.png')
        self.animation=import_folder('./graphics/blood', 0, 0, 110, 93)
        # print(self.animation[0].get_size()[0])



        