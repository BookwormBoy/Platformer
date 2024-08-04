from os import walk
import pygame
from csv import reader
def import_folder(path, cx, cy, w, h):
    surface_list=[]
    for _,__,img_files in walk(path):
        img_files.sort()
        for img in img_files:
            full_path = path+'/'+img
            img_surf=pygame.image.load(full_path).convert_alpha()
            crop=(cx, cy, w, h)
            image_surf=pygame.Surface((w, h), flags=pygame.SRCALPHA)
            image_surf.blit(img_surf, (0, 0), crop)
            image_surf=pygame.transform.scale(image_surf, (w*2, h*2))
            surface_list.append(image_surf)
    return surface_list
    

#import_folder('/home/siddharth-kini/PythonCode/Practice/graphics/idle')

def import_csv_layout(path):
    terrain_map=[]
    with open(path) as map:
        level=reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map