import pygame as pg
import os

class soil:
    def __init__(self,x,y,l):
        self.x=x
        self.y=y
        self.object=pg.Rect(x,y,50,50)
        img=pg.image.load(os.path.join("assets","soil.png"))
        self.image=pg.transform.scale(img,(50,50))
        l.append(self)
    def create(self,window):
        window.blit(self.image,(self.object.x,self.object.y))

class grass:
    def __init__(self,x,y,l):
        self.x=x
        self.y=y
        #self.object=pg.Rect(x,y,50,50)
        self.object=pg.Rect(x,y,50,50)
        img=pg.image.load(os.path.join("assets","grass.png"))
        self.image=pg.transform.scale(img,(50,50))
        #pg.draw.rect(window,(0,0,0),self.object)
        l.append(self)
    def create(self,window):
        window.blit(self.image,(self.object.x,self.object.y))
        #pg.draw.rect(window,(0,255,0),self.object)
