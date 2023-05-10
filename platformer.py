import pygame as pg
import os
import math

player_vel = 3
FPS = 60
WIDTH, HEIGHT = 1000, 700
BG_COLOR = (135, 206, 235)
window = pg.display.set_mode((WIDTH, HEIGHT))

class Player(pg.sprite.Sprite):
    gravity = 0.01
    fall_count=0
    jump = False

    def __init__(self, x, y):
        super().__init__()
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"
        self.mask = None

        self.path = os.path.join("assets","protag.png")
        self.image = pg.image.load(self.path)
        #self.image.convert_alpha()
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))

        self.mask = pg.mask.from_surface(self.image)
        
    def move_player(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def jump_player(self):
        if self.jump:
            self.y_vel = -4.5
            self.jump = False

    def move_left(self):
        if self.direction == "left":
            self.x_vel = -player_vel
        else:
            self.image = pg.transform.flip(self.image, True, False)
            self.direction = "left"
            self.x_vel = -player_vel
    
    def move_right(self):
        if self.direction == "right":
            self.x_vel = player_vel
        else:
            self.image = pg.transform.flip(self.image, True, False)
            self.direction = "right"
            self.x_vel = player_vel
    
    def draw(self,window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def loop(self,fps):
        self.y_vel += min(1,self.gravity * (self.fall_count % fps))
        self.fall_count += 1

    def landed(self):
        self.y_vel = 0
        self.fall_count = 0
        self.jump = True

class Block(pg.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.x = x
        self.y = y
        self.name = name
        self.width = 48
        self.height = 48
        self.path = os.path.join("assets", self.name + ".png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (48, 48))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.mask = pg.mask.from_surface(self.image)

    def draw(self,window):
        window.blit(self.image, (self.x, self.y))

def collidey(player, objs):
    for obj in objs:
        if pg.sprite.collide_mask(player, obj):
            if player.y_vel > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            if player.y_vel < 0:
                player.rect.top = obj.rect.bottom
        
def keybinds(player, objs):
    keys = pg.key.get_pressed()

    player.x_vel = 0
    if keys[pg.K_LEFT]:
        player.move_left()
    
    if keys[pg.K_RIGHT]:
        player.move_right()
    player.move_player()
    collidey(player,objs)
    
def draw(window,player,layer):
    window.fill(BG_COLOR)
    player.draw(window)
    for obj in layer:
        obj.draw(window)
    pg.display.update()

def main(window):
    run = True
    clock = pg.time.Clock()
    player = Player(100, 100)
    block_dimension = 48
    layer0 = [Block(i*block_dimension, HEIGHT-block_dimension, "grass") for i in range(-1,WIDTH//block_dimension +1)]
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    player.jump_player()

        player.loop(FPS)
        keybinds(player, layer0)
        draw(window, player, layer0)
    pg.quit()

if __name__ == "__main__":
    main(window)