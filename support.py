from os import walk
import pygame
def import_folder(path, cx, cy):
    surface_list=[]
    for _,__,img_files in walk(path):
        img_files.sort()
        for img in img_files:
            full_path = path+'/'+img
            img_surf=pygame.image.load(full_path).convert_alpha()
            crop=(cx, cy, 19, 29)
            image_surf=pygame.Surface((19, 30), flags=pygame.SRCALPHA)
            image_surf.blit(img_surf, (0, 0), crop)
            image_surf=pygame.transform.scale(image_surf, (19*2, 30*2))
            surface_list.append(image_surf)
    return surface_list
    

#import_folder('/home/siddharth-kini/PythonCode/Practice/graphics/idle')

