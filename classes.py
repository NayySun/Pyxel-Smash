# The game constants (file modifiable by hand) is imported here to avoid double imports
from game_constants import *


# All the individual classes serving the game engine
class Hitbox:
    def __init__(self, x=-1, y=-1, length=32, height=48):
        self.x = x
        self.y = y
        self.length = length
        self.height = height
    def __str__(self):
        return str((self.x, self.y, self.length, self.height))
    def collide_with(self, object):
        return self.x + self.length > object.x and self.x < object.x + object.length and self.y + self.height > object.y and self.y < object.y + object.height

class Character:
    def __init__(self, name, attack_rank, health_rank, speed_rank, sprites):
        self.name = name
        self.attack_rank = attack_rank
        self.health_rank = health_rank
        self.speed_rank = speed_rank
        self.sprites = sprites
        self.player = None
        self.hitbox = Hitbox()
        self.velocity = 0
        self.on_wall = False
        self.can_jump = True
        self.direction = 0
        self.spawn = (-1, -1)
        self.health = -1
        self.attack = -1
        self.is_punching= False
        self.punch_frame = 0
        self.last_punch = None

    def set_spawn(self, starting_point, length):
        self.hitbox.x, self.hitbox.y = starting_point
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
        self.punch_frame = 0
        if self.direction:
            self.last_punch = Hitbox(self.hitbox.x - (self.hitbox.length/2), self.hitbox.y + 16, self.hitbox.length/2, self.hitbox.height/2)
        else:
            self.last_punch = Hitbox(self.hitbox.x + self.hitbox.length, self.hitbox.y + 16, self.hitbox.length/2, self.hitbox.height/2)
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
    def __init__(self, tilemap, starting_point1, starting_point2, starting_point3, starting_point4, *objects: Object):
        self.tilemap = tilemap
        self.starting_points = starting_point1, starting_point2, starting_point3, starting_point4
        self.objects = objects


# An exemple of a map and a character list, used in the game exemple
map1 = Map(
    0,
    (192, 208), 
    (816, 16), 
    (240, 416), 
    (960, 448), 
    Object(64, 64, 128, 256), 
    Object(448, 64, 128, 256), 
    Object(768, 64, 128, 256), 
    Object(0, 112, 64, 16), 
    Object(192, 256, 128, 16), 
    Object(320, 176, 128, 16), 
    Object(384, 304, 64, 16), 
    Object(576, 64, 128, 16), 
    Object(576, 272, 80, 16), 
    Object(704, 176, 64, 16), 
    Object(896, 112, 64, 16), 
    Object(896, 304, 64, 16),
    Object(0, 384, 64, 192), 
    Object(64, 544, 384, 32), 
    Object(160, 464, 192, 16),
    Object(448, 384, 64, 192), 
    Object(512, 472, 128, 16), 
    Object(704, 448, 64, 128), 
    Object(832, 400, 192, 16), 
    Object(832, 480, 192, 16), 
    Object(832, 560, 192, 16)
)

characters = [
    Character('Fish cat', 3, 3, 3, [(64, 0, 32, 48), (0, 0, 32, 48), (128, 160, 16, 16)]),
    Character('Pumkin cat', 2, 4, 3, [(96, 0, 32, 48), (32, 0, 32, 48), (128, 112, 16, 16)]),
    Character('Devil cat', 5, 1, 2, [(64, 48, 32, 48), (0, 48, 32, 48), (128, 208, 16, 16)]),
    Character('Angel cat', 2, 1, 5, [(96, 48, 32, 48), (32, 48, 32, 48), (128, 192, 16, 16)]),
    Character('Witch cat', 4, 2, 3, [(64, 96, 32, 48), (0, 96, 32, 48), (128, 128, 16, 16)]),
    Character('Princess cat', 2, 3, 4, [(96, 96, 32, 48), (32, 96, 32, 48), (128, 240, 16, 16)]),
    Character('Mafioso cat', 4, 3, 2, [(64, 144, 32, 48), (0, 144, 32, 48), (128, 176, 16, 16)]),
    Character('Box cat', 2, 5, 1, [(96, 144, 32, 48), (32, 144, 32, 48), (0, 240, 16, 16)]),
    Character('Frog cat', 3, 2, 4, [(64, 192, 32, 48), (0, 192, 32, 48), (128, 144, 16, 16)]),
    Character('Ghost cat', 1, 2, 5, [(96, 192, 32, 48), (32, 192, 32, 48), (128, 224, 16, 16)])
]