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
    
def import_cut_graphics(path, block_size):
    surface=pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0]/block_size)
    tile_num_y=int(surface.get_size()[1]/block_size)
    cut_tiles=[]
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x=col*block_size
            y=row*block_size
            new_surf = pygame.Surface((block_size, block_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0,0), pygame.Rect(x,y, block_size, block_size))
            new_surf = pygame.transform.scale(new_surf, (block_size*2, block_size*2))
            cut_tiles.append(new_surf)
    return cut_tiles