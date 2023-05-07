import pygame as pg
import os
from objects import *

objs=[]
velocity=3
WIDTH=900
HEIGHT=500
FPS=60
window=pg.display.set_mode((900,500))
protag_image=pg.image.load(os.path.join("assets","protag.png"))
background_image=pg.image.load(os.path.join("assets","background.png"))
background_image=pg.transform.scale(background_image,(2000,2000))
protag_image=pg.transform.scale(protag_image,(50,50))
left_right=0 #left is 0 and right is 1
def protag_actions(protag_object,keys):
    global left_right
    global protag_image
    if keys[pg.K_UP] and protag_object.y-velocity+10>0:
        movement=True
        for obj in objs:
            if pg.Rect.colliderect(protag_object,obj.object):
                if obj.object.bottom-velocity<=protag_object.top<=obj.object.bottom+velocity:
                    movement=False
                    break
        if movement==True:
            protag_object.y-=velocity
    if keys[pg.K_DOWN] and protag_object.y+velocity+40<500:
        movement=True
        for obj in objs:
            if pg.Rect.colliderect(protag_object,obj.object):
                if obj.object.top-velocity<=protag_object.bottom<=obj.object.top+velocity:
                    movement=False
                break
        if movement==True:
            protag_object.y+=velocity
    if keys[pg.K_LEFT] and protag_object.x-velocity+10>0:
        if left_right==0:
            movement=True
            for obj in objs:
                if pg.Rect.colliderect(protag_object,obj.object):
                    if obj.object.right-velocity<=protag_object.left<=obj.object.right+velocity:
                        movement=False
                    break
            if movement==True:
                protag_object.x-=velocity
        else:
            protag_image=pg.transform.flip(protag_image,True,False)
            movement=True
            for obj in objs:
                if pg.Rect.colliderect(protag_object,obj.object):
                    if obj.object.right-velocity<=protag_object.left<=obj.object.right+velocity:
                        movement=False
                    break
            if movement==True:
                protag_object.x-=velocity
            left_right=0
    if keys[pg.K_RIGHT] and protag_object.x+velocity+40<900:
        if left_right==0:
            protag_image=pg.transform.flip(protag_image,True,False)
            movement=True
            for obj in objs:
                if pg.Rect.colliderect(protag_object,obj.object):
                    movement=False
                    if obj.object.left-velocity<=protag_object.right<=obj.object.left+velocity:
                        movement=False
                    break
            if movement==True:
                protag_object.x+=velocity
            left_right=1
        else:
            movement=True
            for obj in objs:
                if pg.Rect.colliderect(protag_object,obj.object):
                    if obj.object.left-velocity<=protag_object.right<=obj.object.left+velocity:
                        movement=False
                    break
            if movement==True:
                protag_object.x+=velocity
def draw(protag_object):
    window.blit(background_image,(0,0))
    for obj in objs:
        obj.create(window)
    window.blit(protag_image,(protag_object.x,protag_object.y))
    #pg.draw.rect(window,(255,255,255),protag_object)
    pg.display.update()
def make():
    global objs
    g1=grass(200,200,objs)
def main():
    run=True
    clock=pg.time.Clock()
    protag_object=pg.Rect(100,100,50,50)
    make()
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type==pg.QUIT:
                run=False
        keys=pg.key.get_pressed()
        protag_actions(protag_object,keys)
        draw(protag_object)
    pg.quit()
main()