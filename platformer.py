import pygame as pg
import os
import math

from pygame.sprite import AbstractGroup
pg.init()

player_vel = 3
enemy_vel = 1
Font = pg.font.Font("freesansbold.ttf", 10)
FPS = 60
WIDTH, HEIGHT = 1000, 700
BG_COLOR = (135, 206, 235)
window = pg.display.set_mode((WIDTH, HEIGHT))
mainloop = 0  
level_iterator = 0
arrows = []
fireballs = []



class Healthbar:
    def __init__(self):
        self.health = 500
        self.Rect = pg.Rect(250, 0, 500, 20)
        
    def draw(self,window):
        pg.draw.rect(window, (255, 0, 0), self.Rect)

class Staminabar:
    def __init__(self):
        self.stamina = 500
        self.Rect = pg.Rect(250, 20, 500, 20)
        
    def draw(self,window):
        pg.draw.rect(window, (0, 255, 0), self.Rect)

HEALTHBAR = Healthbar()
STAMINABAR = Staminabar()

class Door(pg.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.path = os.path.join("assets", name + ".png")
        img = pg.image.load(self.path)
        self.image = img.convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.image = pg.transform.scale(self.image, (70,70))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pg.mask.from_surface(self.image)
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class EntranceDoor(Door):
    def __init__(self, x, y, name = "entrance_door"):
        super().__init__(x, y, name)
    def draw(self, window):
        return super().draw(window)

class ExitDoor(Door):
    def __init__(self, x, y, name = "exit_door"):
        super().__init__(x, y, name)
    def exit(self, player):
        global level_iterator
        if pg.sprite.collide_mask(self, player):
            level_iterator += 1
            return True
    def draw(self, window):
        return super().draw(window)

class Enemy_Fireball(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.path = os.path.join("assets", "fireball.png")
        img = pg.image.load(self.path)
        self.image = img.convert_alpha()
        self.image = pg.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pg.mask.from_surface(self.image)
        self.direction = direction

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        if self.direction == "right":
            self.rect.x += 4
        elif self.direction == "left":
            self.rect.x -= 4

class Enemy(pg.sprite.Sprite):
    attack_clock = 0
    movement = True
    def __init__(self, x, y, direction):
        super().__init__()
        self.x_vel = 0
        self.y_vel = 0
        self.direction = direction
        self.path = os.path.join("assets","enemy.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image = self.image.convert_alpha()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(topleft = (x, y+15))
        self.mask = pg.mask.from_surface(self.image)
        self.image_direction = "left"
        self.health = 100

    def move_left(self):
        if self.direction == "left" and self.image_direction == "left":
            self.x_vel = -enemy_vel
        else:
            self.image = pg.transform.flip(self.image, True, False)
            self.image.set_colorkey((255,255,255))
            self.image_direction = "left"
            self.x_vel = -enemy_vel

    def move_right(self):
        if self.direction == "right" and self.image_direction == "right":
            self.x_vel = enemy_vel
        else:
            self.image = pg.transform.flip(self.image, True, False)
            self.image.set_colorkey((255,255,255))
            self.image_direction = "right"
            self.x_vel = enemy_vel

    def vision_ai(self, level, player):
        objs = None
        for layer in level:
            if self in layer:
                objs = layer
                break
        if self.direction == "right" and self.attack_clock == 0:
            for obj in objs:
                if player.rect.y-18 <= self.rect.y <= player.rect.y+18:
                    if self.rect.x <= player.rect.x:
                        firing = True
                        for obj in objs:
                            if self.rect.x <= obj.rect.x <= player.rect.x and type(obj) != Enemy:
                                firing = False
                                break
                        if firing:
                            self.enemy_fire()
                            self.attack_clock = 2*FPS
                            break

        elif self.direction == "left" and self.attack_clock == 0:
            for obj in objs:
                if player.rect.y-18 <= self.rect.y <= player.rect.y+18:
                    if player.rect.x <= self.rect.x:
                        firing = True
                        for obj in objs:
                            if player.rect.x <= obj.rect.x <= self.rect.x and type(obj) != Enemy:
                                firing = False
                                break
                        if firing:
                            self.enemy_fire()
                            self.attack_clock = 2*FPS
                            break
 
        else:
            self.attack_clock -= 1

    def reverse_direction(self):
        if self.direction == "right":
            self.direction = "left"
        elif self.direction == "left":
            self.direction = "right"

    def move_enemy(self, vel):
        if self.movement:
            self.rect.x += vel

    def move_ai(self, objs):
        self.move_enemy(self.x_vel)
        for obj in objs:
            if pg.sprite.collide_mask(self, obj) and type(obj) != Enemy:
                self.move_enemy(-self.x_vel)
                self.reverse_direction()
                return None
        
        self.move_enemy(-self.x_vel)
        return None
        
    def enemy_fire(self):
        f = Enemy_Fireball(self.rect.x, self.rect.y, self.direction)
        fireballs.append(f)
        
    def draw(self,window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Arrow(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.direction = direction
        self.path = os.path.join("assets", "arrow.png")
        img = pg.image.load(self.path)
        self.image = img.convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))
        if self.direction == "right":
            self.image.set_colorkey((255, 255, 255))
            self.rect = self.image.get_rect(topleft = (x, y))
            self.mask = pg.mask.from_surface(self.image)
        else:
            self.image = pg.transform.flip(self.image, True, False)
            self.image = self.image.convert_alpha()
            self.image.set_colorkey((255, 255, 255))
            self.rect = self.image.get_rect(topleft = (x, y))
            self.mask = pg.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        if self.direction == "right":
            self.rect.x += 4
        elif self.direction == "left":
            self.rect.x -= 4

    def collision(self, objs):
        for obj in objs:
            if pg.sprite.collide_mask(self, obj):
                if type(obj) == Enemy:
                    obj.health -= 40
                    if obj.health <= 0:
                        objs.remove(obj)
                arrows.remove(self)
    
class Player(pg.sprite.Sprite):
    gravity = 1
    fall_count=0
    jump = False
    Shield = False
    Shield_cooldown_timer = 0
    Shield_working_time = 0

    def attack1(self):
        if STAMINABAR.Rect.width >= 250:
            arrow = Arrow(self.rect.x, self.rect.y, self.direction)
            STAMINABAR.Rect.width -= 250
            arrows.append(arrow)
    
    def shield(self):
        if self.Shield_cooldown_timer == 0 and self.Shield_working_time == 0:
            self.Shield = True
            self.Shield_working_time = 5*FPS
            self.Shield_cooldown_timer = 10*FPS

    def __init__(self, x, y):
        super().__init__()
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"

        self.path = os.path.join("assets","protag.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))
        self.mask = pg.mask.from_surface(self.image)
        
    def move_player(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def jump_player(self):
        if self.jump and STAMINABAR.Rect.width >= 100:
            STAMINABAR.Rect.width -= 100
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
        if self.Shield_working_time == 0:
            self.Shield = False
        if self.Shield_working_time > 0:
            self.Shield_working_time -= 1
        if self.Shield_cooldown_timer > 0 and self.Shield_working_time == 0:
            self.Shield_cooldown_timer -= 1

    def landed(self):
        self.y_vel = 0
        self.fall_count = 0
        self.jump = True

    def head_collide(self):
        self.y_vel = -self.gravity

class Block(pg.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.x = x
        self.y = y
        self.name = name
        self.width = 50
        self.height = 50
        self.path = os.path.join("assets", self.name + ".png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.mask = pg.mask.from_surface(self.image)

    def draw(self,window):
        window.blit(self.image, (self.x, self.y))

class Fireblock(Block):
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
    
    def draw(self, window):
        return super().draw(window)
    
class Fireball(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.path = os.path.join("assets", "fireball.png")
        img = pg.image.load(self.path)
        self.image = img.convert_alpha()
        self.image = pg.transform.scale(self.image, (30,30))
        self.rect = self.image.get_rect(topleft = (x+14, y-25))
        self.mask = pg.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        self.rect.y -= 1

def text(player, window):
    cool_time = Font.render("cooldown: "+str(player.Shield_cooldown_timer//FPS),True, (23,15,236), (255,255,255))
    work_time = Font.render("worktime: "+str(player.Shield_working_time//FPS), True, (45,236,15), (255,255,255))
    shield = None
    if player.Shield == True:
        shield = Font.render("shield: "+"ON", True, (197,173,34), (255,255,255))
    else:
        shield = Font.render("shield: "+"OFF", True, (197,173,34), (255,255,255))
    c = cool_time.get_rect(topleft = (900,10))
    w = work_time.get_rect(topleft = (900,20))
    s = work_time.get_rect(topleft = (900,30))
    window.blit(cool_time, c)
    window.blit(work_time, w)
    window.blit(shield, s)
    
def fire(objs):
    if mainloop%(3*FPS) == 0:
        for obj in objs:
            if type(obj) == Fireblock:
                f = Fireball(obj.x, obj.y)
                fireballs.append(f)

def trap_collision(player, fireballs, objs, HEALTHBAR):
    for fireball in fireballs:
        for obj in objs:
            if pg.sprite.collide_mask(obj, fireball) and type(obj) != Enemy:
                fireballs.remove(fireball)
        if pg.sprite.collide_mask(player, fireball):
            if player.Shield == False:
                HEALTHBAR.Rect.width -= 100
            fireballs.remove(fireball)
                

def collidex(player, objs, vel):
    player.move_player(vel, 0)
    for obj in objs:
        if pg.sprite.collide_mask(player, obj):
            if type(obj) == Enemy:
                HEALTHBAR.Rect.width = 0
            elif type(obj) != EntranceDoor and type(obj) != ExitDoor:
                player.move_player(-vel, 0)
                return True
    
    player.move_player(-vel, 0)
    return False

def collidey(player, objs):
    for obj in objs:
        if pg.sprite.collide_mask(player, obj):
            if type(obj) == Enemy:
                HEALTHBAR.Rect.width = 0
            elif type(obj) != EntranceDoor and type(obj) != ExitDoor:
                if player.y_vel > 0:
                    player.rect.bottom = obj.rect.top
                    player.landed()
                if player.y_vel < 0:
                    player.rect.top = obj.rect.bottom
                    player.head_collide()
        
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
    
def draw(window, player, layers, fireballs, HEALTHBAR, STAMINABAR):
    window.fill(BG_COLOR)
    player.draw(window)
    for obj in layers:
        obj.draw(window)
    for fireball in fireballs:
        fireball.draw(window)
    for arrow in arrows:
        arrow.draw(window)
    text(player, window)
    HEALTHBAR.draw(window)
    STAMINABAR.draw(window)
    pg.display.update()

def obj_mapper(level):
    new_lvl = []
    block_dimension = 50
    for row in range(14):
        new_row = []
        for column in range(20):
            if level[row][column] == 0:
                continue
            elif level[row][column] == 1:
                new_row.append(Block(column*block_dimension, row*block_dimension, "grass"))
            elif level[row][column] == 2:
                new_row.append(Block(column*block_dimension, row*block_dimension, "soil"))
            elif level[row][column] == 3:
                new_row.append(Fireblock(column*block_dimension, row*block_dimension, "fireblock"))
            elif level[row][column] == 4:
                new_row.append(Enemy(column*block_dimension, row*block_dimension, "left"))
            elif level[row][column] == 5:
                new_row.append(Enemy(column*block_dimension, row*block_dimension, "right"))
            elif level[row][column] == 6:
                new_row.append(EntranceDoor(column*block_dimension, row*block_dimension))
            elif level[row][column] == 7:
                new_row.append(ExitDoor(column*block_dimension, row*block_dimension))
        new_lvl.append(new_row)
    return new_lvl

def get_layers(level):
    block_dimension = 50
    layers = []
    for row in level:
        for obj in row:
            layers.append(obj)
    return layers

def enemy_methods(objs, player, level):
    for obj in objs:
        if type(obj) == Enemy:
            obj.vision_ai(level, player)
            obj.move_ai(objs)
            if obj.direction == "left":
                obj.move_left()
            elif obj.direction == "right":
                obj.move_right()
            obj.move_enemy(obj.x_vel)

# row length = 1000/50 = 20
# column length = 700/50 = 14


#grass = 1
#soil = 2
#fireblock = 3
#enemy_left = 4
#enemy_right = 5
#entrance_door = 6
#exit_door = 7


level1 = [
    
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,7],
    [2,1,1,1,1,1,2,1,1,2,2,1,1,1,1,1,1,1,1,2],

]

level2 = [
    
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,1,0,0,0,0,0,0,0,6,0,0,0,0,0,0,1,0,7],
    [2,1,1,1,1,1,2,1,1,2,2,1,1,1,1,1,1,1,1,2],

]

levels = [level1, level2]


def main(window):
    global mainloop
    global fireballs
    global HEALTHBAR
    global STAMINABAR
    global level1
    global level_iterator
    try:
        level = levels[level_iterator]
    except IndexError:
        pg.quit()
    run = True
    clock = pg.time.Clock()
    level_map = obj_mapper(level)
    layers = get_layers(level_map)
    player = None
    entrance_door = None
    exit_door = None
    for obj in layers:
        if type(obj) == EntranceDoor:
            player = Player(obj.rect.x, obj.rect.y)
            entrance_door = obj
        elif type(obj) == ExitDoor:
            exit_door = obj
    while run:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    player.jump_player()
                if event.key == pg.K_SPACE:
                    player.attack1()
                if event.key == pg.K_RSHIFT or event.key == pg.K_LSHIFT:
                    player.shield()

        player.loop(FPS)
        keybinds(player, layers)
        fire(layers)
        for f in fireballs:
            f.move()
        for arrow in arrows:
            arrow.move()
            arrow.collision(layers)
        trap_collision(player, fireballs, layers, HEALTHBAR)
        enemy_methods(layers, player, level_map)
        if exit_door.exit(player):
        ####
            try:
                level = levels[level_iterator]
            except IndexError:
                break
            level_map = obj_mapper(level)
            layers = get_layers(level_map)
            player = None
            entrance_door = None
            exit_door = None
            for obj in layers:
                if type(obj) == EntranceDoor:
                    player = Player(obj.rect.x, obj.rect.y)
                    entrance_door = obj
                elif type(obj) == ExitDoor:
                    exit_door = obj
        ####
        mainloop += 1
        if STAMINABAR.Rect.width < 499:
            STAMINABAR.Rect.width += 1
        draw(window, player, layers, fireballs, HEALTHBAR, STAMINABAR)
        if HEALTHBAR.Rect.width <= 0:
            break

    pg.quit()

if __name__ == "__main__":
    main(window)
