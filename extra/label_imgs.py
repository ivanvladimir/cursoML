#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013 Rogelio Adrian Romero Cordero

import sys, pygame, gc, os
from os import path
from pygame.locals import *


def main():
    screen_size = (800,600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Pruebas Pygame")
    red      = ( 255,   0,   0)
    green      = ( 0,   255,   0)
    blue      = ( 0,   0,   255)

    ###################################
    route_root='test_images'
    route_images=route_root+'/800x600/'
    route_bb=route_root+'/bounding_boxes/'
    ###################################
    index = 0
    file_images = get_filenames(route_images)
    
    background_image = load_image(route_images+file_images[index])
    done=True
    add_polygon=0
    add_head=0
    sum_10=0
    size_draw_pol = 0.5
    size_draw_head = 0.5
    new_rects = []  ##red square
    new_heads = []  ##blue square

    list_pol_h = list_pols_h(route_bb+file_images[index].replace('.jpg','.txt')) ##update polygons and points of head person
    #list_pol_point = list_pols() ##update polygons and points of person
    pol_rect = pygame.Rect(( 1,1 ),( 48*(size_draw_pol),48*(size_draw_pol)))
    while done:
        for eventos in pygame.event.get():
            if eventos.type == pygame.QUIT:
                done=False
      
            if eventos.type == MOUSEMOTION: ##Si el raton se mueve pulsando un boton
                if eventos.buttons[0] and (add_polygon==1 or add_head==1):
                    cur2=pygame.mouse.get_pos()
                    if pol_rect.collidepoint(cur2):
                            pol_rect.left+=eventos.rel[0]
                            pol_rect.top+=eventos.rel[1]
                            
            if eventos.type is KEYDOWN:
                button_pressed = pygame.key.name(eventos.key)
                print button_pressed
                if button_pressed == 'escape':
                    done=False
                if button_pressed == 'q':
                        list_pol_h = []
                        #list_pol_point = []
                        add_polygon=0
                        add_head=0
                if button_pressed == 'a':##add a head point
                        add_head_point=1
                if button_pressed == 'left ctrl':##add a rect
                        if add_polygon==1:
                                new_rects.append(pol_rect)
                                #size_draw_pol=1
                                pol_rect = pygame.Rect((pygame.mouse.get_pos()[0]-24*(size_draw_pol),pygame.mouse.get_pos()[1]-24*(size_draw_pol)),( 48*(size_draw_pol),48*(size_draw_pol) ))
                                add_polygon=0
                        if add_head==1:
                                new_heads.append(pol_rect)
                                print len(new_heads)
                                #size_draw_head=0.5
                                pol_rect = pygame.Rect((pygame.mouse.get_pos()[0]-24*(size_draw_head),pygame.mouse.get_pos()[1]-24*(size_draw_head)),( 48*(size_draw_head),48*(size_draw_head) ))
                                add_head=0
                if button_pressed == 'left shift':
                        if add_polygon==1 and size_draw_pol != 0:
                                size_draw_pol -= 0.1
                                pol_rect = pygame.Rect((pygame.mouse.get_pos()[0]-24*(size_draw_pol),pygame.mouse.get_pos()[1]-24*(size_draw_pol)),( 48*(size_draw_pol),48*(size_draw_pol) ))
                        if add_head==1 and size_draw_head != 0:
                                size_draw_head -= 0.1
                                pol_rect = pygame.Rect((pygame.mouse.get_pos()[0]-24*(size_draw_head),pygame.mouse.get_pos()[1]-24*(size_draw_head)),( 48*(size_draw_head),48*(size_draw_head) ))
                                
                if button_pressed == 'space':##create rect or increase the size of rect (red)
                        if add_head != 1:
                                if add_polygon==1:
                                        size_draw_pol += 0.1
                                        pol_rect = pygame.Rect((pygame.mouse.get_pos()[0]-24*(size_draw_pol),pygame.mouse.get_pos()[1]-24*(size_draw_pol)),( 48*(size_draw_pol),48*(size_draw_pol) ))
                                else:
                                        add_polygon=1
                if button_pressed == 'left alt':
                        if add_polygon != 1:
                                if add_head==1:
                                        size_draw_head += 0.1
                                        pol_rect = pygame.Rect((pygame.mouse.get_pos()[0]-24*(size_draw_head),pygame.mouse.get_pos()[1]-24*(size_draw_head)),( 48*(size_draw_head),48*(size_draw_head) ))
                                else:
                                        add_head=1
                if button_pressed == 'x':##delete the last polygon (red)
                        if len(new_rects) != 0:
                              new_rects.pop()  
                if button_pressed == 's':##delete the last polygon (blue)
                        if len(new_heads) != 0:
                                new_heads.pop()
                if button_pressed == 'right' or button_pressed == 'left':
                        
                        add_polygon=0
                        add_head_point=0
                        add_head=0
                        size_draw_pol = 0.5
                        size_draw_head = 0.5
                        pol_rect = pygame.Rect(( 1,1 ),( 48*(size_draw_pol),48*(size_draw_pol) ))
                        new_rects = []
                        new_heads = []
                        new_head_points = []
                        if button_pressed == 'right':##next image
                            if index != len(file_images):
                                index+=1
                            if not(index +10 >= len(file_images)) and sum_10==1:
                                index+=9
                        if button_pressed == 'left':##previous image
                            if index != 0:
                                index-=1
                            if not(index -10 < 0)and sum_10==1:
                                index-=9
                        background_image = load_image(route_images+file_images[index])
                        screen = pygame.display.set_mode((background_image.get_width(), background_image.get_height()))
                        list_pol_h = list_pols_h(route_bb+file_images[index].replace('.jpg','.txt'))
                        #list_pol_point = list_pols(sing_file)
                        pygame.display.set_caption("Imagen "+str(index+1))
                        ##pygame.display.set_caption("Imagen "+lineas_img[index].replace('\n',''))
###################################################
              
                if button_pressed == 'return':
                        cad_h=''
                        new_file_h = open (route_bb+file_images[index].replace('.jpg','.txt'), "w")
                        #new_file = open (file_to_open, "w")
                        for i in range(len(new_heads)):
                                cad_h+=str(new_heads[i].topleft[0])+'\t'+str(new_heads[i].topleft[1])+'\t'+str(new_heads[i].bottomright[0])+'\t'+str(new_heads[i].bottomright[1])+'\n'
                        new_file_h.write(cad_h)
                        new_file_h.close()
                        add_polygon=0
                        add_head_point=0
                        add_head=0
                        list_pol_h = []
                        new_head_points = []
                        #list_pol_point = [[],list_pol_point[1]]
                        size_draw_pol = 0.5
                        size_draw_head = 0.5
                        pol_rect = pygame.Rect(( 1,1 ),( 48*(size_draw_pol),48*(size_draw_pol) ))

        screen.blit(background_image, ( 0, 0))
            ##pygame.draw.rect(screen,red,rect)
        for head in list_pol_h:
                pygame.draw.polygon(screen, blue, head, 1)
        for polygon in new_rects:
                pygame.draw.rect(screen, red, polygon, 1)
        for head in new_heads:
                pygame.draw.rect(screen, blue, head, 1)
        #for pol in list_pol_point[0]:
                #pygame.draw.polygon(screen, red, pol, 1)
        #for point in list_pol_point[1]:
                #pygame.draw.circle(screen, red, point, 2, 2)
        if add_polygon==1:
                pygame.draw.rect(screen, green, pol_rect,1)
        if add_head==1:
                pygame.draw.rect(screen, green, pol_rect,1)
        pygame.display.update(background_image.get_rect());
    pygame.quit()

def load_image(filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error, message:
            raise SystemExit, message
    image = image.convert()
    if transparent:
            color = image.get_at((0,0))
            image.set_colorkey(color, RLEACCEL)
    return image

    
def get_filenames(_route):
    files = os.listdir(_route)
    return files

def list_pols(list_file):
        list_pol1 = []
        list_point1 = []
        list_eve = []
        for linea in list_file:                        
            ls=linea.split()
            if(len(ls) >= 4):
                point1 = (int(ls[0]),int(ls[1]))
                point3 = (int(ls[2]),int(ls[3]))
                point2 = (point1[0],point3[1])
                point4 = (point3[0],point1[1])
                if( int(ls[2]) != 0 and int(ls[2]) != 0 ):
                        list_pol1.append([point1,point2,point3,point4,point1])
        list_eve.append(list_pol1)
        list_eve.append(list_point1)
        return list_eve

def list_pols_h(name_file_abs):
        list_pol1 = []
        if path.exists(name_file_abs) and path.isfile(name_file_abs):
            file1 = open(name_file_abs)
            lineas = file1.readlines()
            for linea in lineas:                        
                ls=linea.split()
                if(len(ls) >= 4):
                    point1 = (int(ls[0]),int(ls[1]))
                    point3 = (int(ls[2]),int(ls[3]))
                    point2 = (point1[0],point3[1])
                    point4 = (point3[0],point1[1])
                    if( int(ls[2]) != 0 and int(ls[2]) != 0 ):
                        list_pol1.append([point1,point2,point3,point4,point1]) 
        return list_pol1

if __name__ == '__main__':
    pygame.init()
    main()


























                
