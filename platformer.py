import pygame as pg
import os
import tkinter as tk

pg.init()

player_vel = 3
enemy_vel = 1
Font = pg.font.Font("freesansbold.ttf", 10)
FPS = 60
WIDTH, HEIGHT = 1000, 700
BG_COLOR = (135, 206, 235)
mainloop = 0  
level_iterator = 0
arrows = []
fireballs = []


class Healthbar:
    # this is the healthbar of the player
    # doesn't get regenerated
    # total initial health is 500
    def __init__(self):
        self.health = 500
        self.Rect = pg.Rect(250, 0, 500, 20)
        
    def draw(self, window):
        pg.draw.rect(window, (255, 0, 0), self.Rect)


class Staminabar:
    # this is the staminabar of player. when player attacks or jumps or uses shield, stamina gets consumed
    # gets regenerated
    # total initial health is 500
    def __init__(self):
        self.stamina = 500
        self.Rect = pg.Rect(250, 20, 500, 20)
        
    def draw(self, window):
        pg.draw.rect(window, (0, 255, 0), self.Rect)


HEALTHBAR = Healthbar()
STAMINABAR = Staminabar()


class Door(pg.sprite.Sprite):
    # this class is parent class to entrance door and exit door
    def __init__(self, x, y, name):
        super().__init__()
        self.path = os.path.join("assets", name + ".png")
        img = pg.image.load(self.path)
        self.image = img.convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.image = pg.transform.scale(self.image, (70, 70))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pg.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


class EntranceDoor(Door):
    # the player spawns here. The player can move through this
    def __init__(self, x, y, name="entrance_door"):
        super().__init__(x, y, name)

    def draw(self, window):
        return super().draw(window)


class ExitDoor(Door):
    # this is the objective of the level. touching this will move to another level if any
    def __init__(self, x, y, name="exit_door"):
        super().__init__(x, y, name)

    def exit(self, player):
        global level_iterator
        if pg.sprite.collide_mask(self, player):
            level_iterator += 1
            return True

    def draw(self, window):
        return super().draw(window)


class Enemy_Fireball(pg.sprite.Sprite):
    # this is the class of fireball emitted by enemies
    # unlike other fireball that comes out of traps, this moves horizontally
    # when player touches it, the health bar is reduced by 100
    def __init__(self, x, y, direction):
        super().__init__()
        self.path = os.path.join("assets", "fireball.png")
        img = pg.image.load(self.path)
        self.image = img.convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pg.mask.from_surface(self.image)
        self.direction = direction

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        if self.direction == "right":
            self.rect.x += 4
        elif self.direction == "left":
            self.rect.x -= 4

    def collision(self, objs, player):
        for obj in objs:
            if pg.sprite.collide_mask(self, obj) and type(obj) != EntranceDoor and type(obj) != ExitDoor and type(obj) != Enemy:
                fireballs.remove(self)
                break
            elif pg.sprite.collide_mask(self, player):
                if not player.Shield:
                    HEALTHBAR.Rect.width -= 100
                fireballs.remove(self)
                break

class Enemy(pg.sprite.Sprite):
    # this is the class of the enemy unit
    attack_clock = 0
    movement = True

    def __init__(self, x, y, direction):
        super().__init__()
        self.x_vel = 0
        self.y_vel = 0
        self.direction = direction
        self.path = os.path.join("assets", "enemy.png")
        self.image = pg.image.load(self.path)
        self.image = pg.transform.scale(self.image, (32, 32))
        self.image = self.image.convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(topleft=(x, y+15))
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
        # this defines the line of sight of the enemy
        # if the player is in the line of sight of the enemy, that is
        # the player is in the same row as enemy and in the direction of enemy then the enemy unit
        # fires a fireball towards the player
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
                            if self.rect.x <= obj.rect.x <= player.rect.x and type(obj) != Enemy and type(obj) != EntranceDoor and type(obj) != ExitDoor:
                                firing = False
                                break
                        if firing:
                            self.enemy_fire()
                            self.attack_clock = 0.75*FPS
                            break

        elif self.direction == "left" and self.attack_clock == 0:
            for obj in objs:
                if player.rect.y-18 <= self.rect.y <= player.rect.y+18:
                    if player.rect.x <= self.rect.x:
                        firing = True
                        for obj in objs:
                            if player.rect.x <= obj.rect.x <= self.rect.x and type(obj) != Enemy and type(obj) != EntranceDoor and type(obj) != ExitDoor:
                                firing = False
                                break
                        if firing:
                            self.enemy_fire()
                            self.attack_clock = 0.75*FPS
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
        # this is for detecting collision with blocks. if the enemy unit collides with a block it will
        # reverse its direction
        self.move_enemy(self.x_vel)
        for obj in objs:
            if pg.sprite.collide_mask(self, obj) and type(obj) != Enemy and type(obj) != EntranceDoor and type(obj) != ExitDoor:
                self.move_enemy(-self.x_vel)
                self.reverse_direction()
                return None
        
        self.move_enemy(-self.x_vel)
        return None
        
    def enemy_fire(self):
        # this is the function that makes enemy fire the firballs
        f = Enemy_Fireball(self.rect.x, self.rect.y, self.direction)
        fireballs.append(f)
        
    def draw(self,window):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Arrow(pg.sprite.Sprite):
    # this is the player's weapon
    # costs 250 stamina, that is half of total stamina
    # deals 40 damage to enemy unit, need 3 hits to kill one unit
    # if it collides with a block, it will disappear
    def __init__(self, x, y, direction):
        super().__init__()
        self.direction = direction
        self.path = os.path.join("assets", "arrow.png")
        img = pg.image.load(self.path)
        self.image = img.convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))
        if self.direction == "right":
            self.image.set_colorkey((255, 255, 255))
            self.rect = self.image.get_rect(topleft=(x, y))
            self.mask = pg.mask.from_surface(self.image)
        else:
            self.image = pg.transform.flip(self.image, True, False)
            self.image = self.image.convert_alpha()
            self.image.set_colorkey((255, 255, 255))
            self.rect = self.image.get_rect(topleft=(x, y))
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
            if pg.sprite.collide_mask(self, obj) and type(obj) != EntranceDoor and type(obj) != ExitDoor:
                if type(obj) == Enemy:
                    obj.health -= 40
                    if obj.health <= 0:
                        objs.remove(obj)
                arrows.remove(self)
        for fireball in fireballs:
            if pg.sprite.collide_mask(self, fireball):
                fireballs.remove(fireball)
                arrows.remove(self)


class Player(pg.sprite.Sprite):
    gravity = 1
    fall_count=0
    jump = False
    Shield = False
    Shield_cooldown_timer = 0
    Shield_working_time = 0
    # this is our player object

    def attack1(self):
        # this is the attack function. if player presses space he fires an arrow
        # in the direction that he is facing
        if STAMINABAR.Rect.width >= 250:
            arrow = Arrow(self.rect.x, self.rect.y+5, self.direction)
            STAMINABAR.Rect.width -= 250
            arrows.append(arrow)
    
    def shield(self):
        # this is the shield function. if player presses shift he will activate a shield
        # that will last for 5 seconds and costs 450 stamina. it has a cooldown of 45 seconds
        # that begins after the shield disappears
        if self.Shield_cooldown_timer == 0 and self.Shield_working_time == 0 and STAMINABAR.Rect.width >= 450:
            STAMINABAR.Rect.width -= 450
            self.Shield = True
            self.Shield_working_time = 5*FPS
            self.Shield_cooldown_timer = 45*FPS
            self.path = os.path.join("assets", "shielded_protag.png")
            self.image = pg.image.load(self.path)
            self.image = self.image.convert_alpha()
            if self.direction == "left":
                self.image = pg.transform.flip(self.image, True, False)
            self.image = pg.transform.scale(self.image, (35, 35))
            self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
            self.mask = pg.mask.from_surface(self.image)

    def __init__(self, x, y):
        super().__init__()
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "right"
        self.path = os.path.join("assets", "protag.png")
        self.image = pg.image.load(self.path)
        self.image = self.image.convert_alpha()
        self.image = pg.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pg.mask.from_surface(self.image)
        
    def move_player(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def jump_player(self):
        # if the player presses up arrow: he jumps
        # costs 100 stamina
        if self.jump and STAMINABAR.Rect.width >= 100:
            STAMINABAR.Rect.width -= 100
            self.y_vel = -16
            self.jump = False

    def move_left(self):
        # self explanatory
        if self.direction == "left":
            self.x_vel = -player_vel
        else:
            self.image = pg.transform.flip(self.image, True, False)
            self.direction = "left"
            self.x_vel = -player_vel
    
    def move_right(self):
        # self explanatory
        if self.direction == "right":
            self.x_vel = player_vel
        else:
            self.image = pg.transform.flip(self.image, True, False)
            self.direction = "right"
            self.x_vel = player_vel
    
    def draw(self,window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def loop(self,fps):
        # works with in-game time defined on FPS
        self.y_vel += min(1, self.fall_count)*self.gravity
        self.fall_count += 1
        if self.Shield_working_time == 0:
            self.Shield = False
            self.path = os.path.join("assets", "protag.png")
            self.image = pg.image.load(self.path)
            self.image = self.image.convert_alpha()
            if self.direction == "left":
                self.image = pg.transform.flip(self.image, True, False)
            self.image = pg.transform.scale(self.image, (35, 35))
            self.rect = self.image.get_rect(topleft = (self.rect.x, self.rect.y))
            self.mask = pg.mask.from_surface(self.image)
        if self.Shield_working_time > 0:
            self.Shield_working_time -= 1
        if self.Shield_cooldown_timer > 0 and self.Shield_working_time == 0:
            self.Shield_cooldown_timer -= 1

    def landed(self):
        # the player can only jump if is on the ground
        # this defines the condition for player to be on the ground
        self.y_vel = 0
        self.fall_count = 0
        self.jump = True

    def head_collide(self):
        # if the player hits his head on the block above him, then he will start moving downwards
        self.y_vel = -self.gravity

class Block(pg.sprite.Sprite):
    # self explanatory
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
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pg.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))


class Fireblock(Block):
    # this is trap that fires fireballs upwards
    def __init__(self, x, y, name):
        super().__init__(x, y, name)
    
    def draw(self, window):
        return super().draw(window)


class Fireball(pg.sprite.Sprite):
    # this is the fireball that moves in y-direction
    def __init__(self, x, y):
        super().__init__()
        self.path = os.path.join("assets", "fireball.png")
        img = pg.image.load(self.path)
        self.image = img.convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=(x+14, y-25))
        self.mask = pg.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def move(self):
        self.rect.y -= 1

    def collision(self, objs, player):
        for obj in objs:
            if pg.sprite.collide_mask(self, obj) and type(obj) != EntranceDoor and type(obj) != ExitDoor and type(obj) != Enemy:
                fireballs.remove(self)
                break
            elif pg.sprite.collide_mask(self, player):
                if not player.Shield:
                    HEALTHBAR.Rect.width -= 100
                fireballs.remove(self)
                break


def text(player, window):
    # this the function to generate text about player's shield status
    cool_time = Font.render("cooldown: "+str(player.Shield_cooldown_timer//FPS),True, (23, 15, 236), (255, 255, 255))
    work_time = Font.render("worktime: "+str(player.Shield_working_time//FPS), True, (45, 236, 15), (255, 255, 255))
    shield = None
    if player.Shield == True:
        shield = Font.render("shield: "+"ON", True, (197, 173, 34), (255, 255, 255))
    else:
        shield = Font.render("shield: "+"OFF", True, (197, 173, 34), (255, 255, 255))
    c = cool_time.get_rect(topleft=(900, 10))
    w = work_time.get_rect(topleft=(900, 20))
    s = work_time.get_rect(topleft=(900, 30))
    window.blit(cool_time, c)
    window.blit(work_time, w)
    window.blit(shield, s)


def fire(objs):
    # this function is for fireblock objects
    if mainloop%(1.5*FPS) == 0:
        for obj in objs:
            if type(obj) == Fireblock:
                f = Fireball(obj.x, obj.y)
                fireballs.append(f)

                
# initially we were facing trouble with collisions and jumping so we took help from
# a youtube video, we will give it's reference in the readme file


def collidex(player, objs, vel):
    # this defines collision in x direction
    # every frame this will move the player in his direction by vel pixels
    # if he is colliding with an block his movement will stop
    # if he collides with an enemy then the game will end
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
    # this defines collision in y direction
    # again if the player collides with the enemy: he dies
    # if while moving vertically in a some direction the player collides with a block then he is
    # translated accordingly
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
    # these are key presses corresponding to movement
    # left arrow corresponds to left movement... the rest is obvious
    keys = pg.key.get_pressed()
    collide_right = collidex(player, objs, player_vel)
    collide_left = collidex(player, objs, -player_vel)
    player.x_vel = 0
    if keys[pg.K_LEFT] and not collide_left:
        player.move_left()
    
    if keys[pg.K_RIGHT] and not collide_right:
        player.move_right()
    player.move_player(player.x_vel, player.y_vel)
    collidey(player, objs)


def draw(window, player, layers, fireballs, HEALTHBAR, STAMINABAR):
    # this function draws images onto the screen
    window.fill(BG_COLOR)
    for obj in layers:
        obj.draw(window)
    for fireball in fireballs:
        fireball.draw(window)
    for arrow in arrows:
        arrow.draw(window)
    text(player, window)
    HEALTHBAR.draw(window)
    STAMINABAR.draw(window)
    player.draw(window)

    pg.display.update()


def obj_mapper(level):
    # this function creates a matrix of objects from a matrix of integers
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
    # this function converts 2D object matrix to 1 dimensional list
    block_dimension = 50
    layers = []
    for row in level:
        for obj in row:
            layers.append(obj)
    return layers


def enemy_methods(objs, player, level):
    # this combines all the methods used by enemy class into one function and applies
    # it to all enemy objects
    for obj in objs:
        if type(obj) == Enemy:
            obj.vision_ai(level, player)
            obj.move_ai(objs)
            if obj.direction == "left":
                obj.move_left()
            elif obj.direction == "right":
                obj.move_right()
            obj.move_enemy(obj.x_vel)

LAUNCH = False


class MAIN_MENU:
    # this is the main menu class made in tkinter
    # it has two buttons: start & quit
    def __init__(self):
        self.main_menu = tk.Tk()
        self.main_menu.geometry("400x400")
        self.main_menu.configure(bg = "light blue")
        self.main_menu.title("Platformer")
        self.start = tk.Button(self.main_menu, text="START", cursor="hand1",width=35, height=3, command=self.launch, foreground="green", background="navajo white")
        self.exit = tk.Button(self.main_menu, text="QUIT", cursor="pirate", width=35, height=3, command=self.main_menu.destroy, foreground="red", background="navajo white")
        self.start.place(x=45, y=100)
        self.exit.place(x=45, y=200)
        tk.mainloop()

    def launch(self):
        global LAUNCH

        self.main_menu.destroy()
        LAUNCH = True


def victory():
    # if the player wins the game then a window will pop up saying  "!! YOU WIN :) !!"
    triumph = tk.Tk()
    triumph.geometry("300x300")
    triumph.title("VICTORY !!")

    victory_text = tk.Label(triumph, text="!! YOU WIN :) !!", foreground="green")
    victory_text.place(x=85, y=25)
    tk.mainloop()


def loss():
    # if the player loses the game then a window will pop up saying "!! YOU LOSE :( !!"
    defeat = tk.Tk()
    defeat.title("DEFEAT !!")
    defeat.geometry("300x300")

    loss_text = tk.Label(defeat, text="!! YOU LOSE :( !!", foreground="red")
    loss_text.place(x=85, y=25)
    tk.mainloop()

# row length = 1000/50 = 20
# column length = 700/50 = 14


# grass = 1
# soil = 2
# fireblock = 3
# enemy_left = 4
# enemy_right = 5
# entrance_door = 6
# exit_door = 7

# the below are level matrices and above are instructions
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
    [2,0,1,0,0,0,4,0,0,0,6,0,0,0,1,0,0,1,0,7],
    [2,1,1,1,1,1,2,1,1,2,2,1,1,1,1,1,1,1,1,2],

]

level3 = [
    
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,1,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,1,1,1,1,3,1,1,3,1,1,3,1,1,1,1,1,1,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,1,1,1,1,1,1,1,1,1,1,3,1,1,1,1,1,1,0,2],
    [2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,1,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,1,1,2],

]

level4 = [
    
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,1,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,1,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,2],
    [2,0,1,1,1,1,3,1,1,3,1,1,3,1,1,1,1,1,1,2],
    [2,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
    [2,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,1,1,1,1,1,1,1,1,1,1,3,1,1,1,1,1,1,0,2],
    [2,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,1,1,1,1,1,1,1,1,3,1,1,1,1,1,1,1,1,3,2],

]

level5 = [
    
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,5,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,4,2],
    [2,0,0,2,2,2,2,2,2,2,2,0,2,2,2,2,2,2,2,2],
    [2,6,1,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,7,2],
    [2,1,2,1,1,1,2,1,1,2,2,1,1,1,1,1,1,1,1,2],

]

level6 = [# BY DHRUVADEEP
    
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,2],
    [2,0,0,4,0,0,0,0,0,4,0,0,0,0,0,0,1,1,1,2],
    [2,0,1,1,1,0,0,0,1,1,1,1,3,1,1,1,1,1,0,2],
    [2,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,2],
    [2,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [2,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,2],
    [2,1,1,1,1,1,2,1,1,2,2,1,1,1,1,1,1,1,1,2],

]

level7 = [
    
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
    [2,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,2],
    [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2],
    [2,1,0,0,1,1,0,0,1,0,0,1,0,0,0,0,0,1,0,2],
    [2,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,2],
    [2,0,0,1,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],
    [2,6,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,2],
    [2,1,2,1,1,1,3,3,1,2,2,1,1,1,1,1,1,1,1,2],

]

levels = [level1, level2, level3, level4, level5, level6, level7]

menu = MAIN_MENU()


def main():

    # this is the main function
    global mainloop
    global fireballs
    global HEALTHBAR
    global STAMINABAR
    global level1
    global level_iterator
    global menu
    global arrows
    global fireballs

    window = pg.display.set_mode((WIDTH, HEIGHT))
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
    player = Player(0,0)
    for obj in layers:
        if type(obj) == EntranceDoor:
            player.rect.x = obj.rect.x; player.rect.y = obj.rect.y
            entrance_door = obj
        elif type(obj) == ExitDoor:
            exit_door = obj
    while run:
        if level_iterator == 5:
            pg.display.set_caption("LVL 6 by Dhruv")
        else:
            pg.display.set_caption(f"LVL {level_iterator+1}")
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
            f.collision(layers, player)
        for arrow in arrows:
            arrow.move()
            arrow.collision(layers)
        enemy_methods(layers, player, level_map)
        if exit_door.exit(player):
            try:
                arrows = []
                fireballs = []
                level = levels[level_iterator]
            except IndexError:
                victory()
                break
            level_map = obj_mapper(level)
            layers = get_layers(level_map)
            entrance_door = None
            exit_door = None
            for obj in layers:
                if type(obj) == EntranceDoor:
                    player.rect.x = obj.rect.x; player.rect.y = obj.rect.y
                    entrance_door = obj
                elif type(obj) == ExitDoor:
                    exit_door = obj
        mainloop += 1
        if STAMINABAR.Rect.width < 499:
            STAMINABAR.Rect.width += 1
        text(player, window)
        draw(window, player, layers, fireballs, HEALTHBAR, STAMINABAR)
        if HEALTHBAR.Rect.width <= 0:
            loss()
            break

    pg.quit()


if LAUNCH:
    main()
