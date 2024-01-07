from game_constants import *

class Hitbox:
    def __init__(self, x=-1, y=-1, length=32, height=32):
        self.x = x
        self.y = y
        self.length = length
        self.height = height
    def __str__(self):
        return str((self.x, self.y, self.length, self.height))
    def collide_with(self, object):
        return self.x + self.length > object.x and self.x < object.x + object.length and self.y + self.height > object.y and self.y < object.y + object.height

class Character:
    def __init__(self, name, attack_rank, health_rank, speed_rank, size_multiplier, sprites):
        self.name = name
        self.attack_rank = attack_rank
        self.health_rank = health_rank
        self.speed_rank = speed_rank
        self.size_multiplier = size_multiplier
        self.sprites = sprites
        self.hitbox = Hitbox()
        self.velocity = 0
        self.on_wall = False
        self.can_jump = True
        self.punch_cooldown = 0
        self.direction = 0
        self.spawn = (-1, -1)
        self.health = -1
        self.attack = -1
        self.is_punching= False
        self.last_punch = None

    def set_spawn(self, starting_point, length):
        self.hitbox.x, self.hitbox.y = starting_point
        self.hitbox.length *= self.size_multiplier
        self.hitbox.height *= self.size_multiplier
        self.spawn = starting_point
        self.health = round(HEALTH*self.health_rank/3)
        self.attack = round(ATTACK*self.attack_rank/3)
        if self.hitbox.x >= length/2:
            self.direction = 1 

    def move_right(self, objects):
        self.direction = 0
        self.on_wall = False
        self.hitbox.x += SPEED+self.speed_rank
        for object in objects:
            if self.hitbox.collide_with(object.hitbox):
                while self.hitbox.collide_with(object.hitbox):
                    self.hitbox.x -= 1
                self.on_wall = True
                self.velocity = 0
                self.can_jump = True

    def move_left(self, objects):
        self.direction = 1
        self.on_wall = False
        self.hitbox.x -= SPEED+self.speed_rank
        for object in objects:
            if self.hitbox.collide_with(object.hitbox):
                while self.hitbox.collide_with(object.hitbox):
                    self.hitbox.x += 1
                self.on_wall = True
                self.velocity = 0
                self.can_jump = True

    def move_down(self):
        self.on_wall = False
        self.can_jump = False
        if self.velocity < SPEED_CAP:
            self.velocity += GRAVITY

    def move_up(self):
        if self.can_jump:
            self.velocity = -3*(SPEED*4+self.speed_rank/6)
            if self.velocity < -1*SPEED_CAP:
                self.velocity = -1*SPEED_CAP
            self.can_jump = False

    def fall(self, objects, height):
        if self.velocity < SPEED_CAP:
            self.velocity += GRAVITY
        if not self.on_wall:
            self.hitbox.y += self.velocity
            if self.velocity >= 3:
                self.can_jump = False
            for object in objects:
                if self.hitbox.collide_with(object.hitbox):
                    while self.hitbox.collide_with(object.hitbox):
                        if self.velocity < 0:
                            self.hitbox.y += 1
                        else:
                            self.hitbox.y -= 1
                            self.can_jump = True
                    self.velocity = 0
        if self.hitbox.y > height:
            self.hitbox.x, self.hitbox.y = self.spawn

    def punch(self, characters):
        self.is_punching = True
        self.punch_cooldown = 3
        if self.direction:
            self.last_punch = Hitbox(self.hitbox.x - (self.hitbox.length/2), self.hitbox.y + (self.hitbox.height/4), self.hitbox.length/2, self.hitbox.height/2)
        else:
            self.last_punch = Hitbox(self.hitbox.x + self.hitbox.length, self.hitbox.y + (self.hitbox.height/4), self.hitbox.length/2, self.hitbox.height/2)
        for character in characters:
            if character.hitbox.collide_with(self.last_punch):
                character.health -= self.attack
                if character.health <= 0:
                    character.health = 0
#                    character.die()
                    characters.remove(character)
        

class Object:
    def __init__(self, x, y, length, height):
        self.hitbox = Hitbox()
        self.hitbox.x, self.hitbox.y, self.hitbox.length, self.hitbox.height = x, y, length, height

class Map:
    def __init__(self, starting_point1, starting_point2, starting_point3, starting_point4, *objects: Object):
        self.starting_points = starting_point1, starting_point2, starting_point3, starting_point4
        self.objects = objects

map1 = Map(
    (192, 224), 
    (864, 120), 
    (544, 32), 
    (576, 448), 
    Object(64, 64, 96, 256), 
    Object(416, 64, 96, 256), 
    Object(736, 64, 96, 256), 
    Object(0, 384, 64, 192), 
    Object(160, 256, 128, 32), 
    Object(352, 128, 64, 32), 
    Object(352, 288, 64, 32), 
    Object(512, 64, 96, 32), 
    Object(512, 256, 96, 32), 
    Object(672, 160, 64, 32), 
    Object(832, 80, 64, 32), 
    Object(832, 272, 64, 32), 
    Object(64, 544, 384, 32), 
    Object(128, 448, 160, 32),
    Object(448, 384, 64, 192), 
    Object(512, 480, 192, 32), 
    Object(768, 448, 64, 96), 
    Object(896, 384, 128, 32), 
    Object(896, 464, 128, 32), 
    Object(896, 544, 128, 32)
)

characters = [Character('blue slime', 3, 3, 3, 1, [(0, 0, 32, 32), (32, 0, 32, 32), (64, 0, 16, 16)]), Character('red demon', 5, 1, 2, 1, [(0, 32, 32, 32), (32, 32, 32, 32), (64, 32, 16, 16)]), Character('green slime', 4, 5, 2, 1, [(0, 64, 32, 32), (32, 64, 32, 32), (64, 64, 16, 16)]), Character('purple demon', 2, 1, 5, 1, [(0, 96, 32, 32), (32, 96, 32, 32), (64, 96, 16, 16)])]