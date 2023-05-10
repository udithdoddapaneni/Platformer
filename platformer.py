import pygame as pg
import os
import math

player_vel = 3
FPS = 60
WIDTH, HEIGHT = 1000, 700
BG_COLOR = (135, 206, 235)
window = pg.display.set_mode((WIDTH, HEIGHT))

class Player(pg.sprite.Sprite):
    gravity = 1
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
        
    def move_player(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def jump_player(self):
        if self.jump:
            self.y_vel = -16
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
        self.y_vel += min(1, (self.fall_count))*self.gravity
        self.fall_count += 1

    def landed(self):
        self.y_vel = 0
        self.fall_count = 0
        self.jump = True

    def head_collide(self):
        self.y_vel *= -1

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

def collidex(player, objs, vel):
    player.move_player(vel, 0)
    for obj in objs:
        if pg.sprite.collide_mask(player, obj):
            player.move_player(-vel, 0)
            return True
    
    player.move_player(-vel, 0)
    return False

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
    collide_right = collidex(player, objs, player_vel)
    collide_left = collidex(player, objs, -player_vel)
    player.x_vel = 0
    if keys[pg.K_LEFT] and not collide_left:
        player.move_left()
    
    if keys[pg.K_RIGHT] and not collide_right:
        player.move_right()
    player.move_player(player.x_vel, player.y_vel)
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
    layer0 = [Block(500, HEIGHT-2*block_dimension, "grass")]+[Block(300, HEIGHT-3*block_dimension, "grass")] + [Block(i*block_dimension, HEIGHT-block_dimension, "grass") for i in range(-1,WIDTH//block_dimension +1)]
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
