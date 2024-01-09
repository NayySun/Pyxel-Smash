# All the imports
from classes import *
import pyxel as p
import json


# The game engine made using pyxel
class Game:
    def __init__(self, map: Map, characters: Character):
        p.init(SCREEN_LENGTH, SCREEN_HEIGHT, 'Game', 60) # Init pyxel
        p.load('resources.pyxres')
        self.game_start = False
        self.menu = 0
        self.nb_player = 2
        self.map = map
        self.clock = 0
        with open('mapping.json', 'r') as file: # Get the mapping as a dictionnary
            self.mapping = json.load(file)
        self.characters = characters
        self.selected_characters = [self.characters[i] for i in range(self.nb_player)]
        p.run(self.update, self.draw)

    def update(self):
        self.clock += 1
        if self.game_start: # This is the update during the game
            for character in self.characters:
                if p.btn(eval(f'p.{self.mapping[character.player]["right"]}')): # 
                    character.move_right(self.map.objects)
                if p.btn(eval(f'p.{self.mapping[character.player]["left"]}')):
                    character.move_left(self.map.objects)
                if p.btn(eval(f'p.{self.mapping[character.player]["up"]}')):
                    character.move_up()
                if p.btn(eval(f'p.{self.mapping[character.player]["down"]}')):
                    character.move_down()
                character.fall(self.map.objects, p.height)
                if p.btn(eval(f'p.{self.mapping[character.player]["attack"]}')) and not character.is_punching and not character.on_wall:
                    character.punch(self.characters)
                if character.is_punching:
                    character.punch_frame += 1
                    if character.punch_frame == 8:
                        character.punch_frame = 0
                        character.last_punch = None
                        character.is_punching = False
            if len(self.characters) == 1:
                self.game_start = False    
        else:
            if self.menu == 0: # This is the update for each individual menu
                if p.btn(p.MOUSE_BUTTON_LEFT):
                    self.menu += 1
            if self.menu == 1:
                if p.btn(p.MOUSE_BUTTON_LEFT) and p.mouse_x > p.width/2-50 and p.mouse_x < p.width/2-34 and p.mouse_y > 50 and p.mouse_y < 64 and self.nb_player > 2 and self.clock%4 == 0:
                    self.nb_player -= 1
                    self.selected_characters = [self.characters[i] for i in range(self.nb_player)]
                if p.btn(p.MOUSE_BUTTON_LEFT) and p.mouse_x > p.width/2+50 and p.mouse_x < p.width/2+64 and p.mouse_y > 50 and p.mouse_y < 64 and self.nb_player < 4 and self.clock%4 == 0:
                    self.nb_player += 1
                    self.selected_characters = [self.characters[i] for i in range(self.nb_player)]
                for i in range(self.nb_player):
                    if p.btn(p.MOUSE_BUTTON_LEFT) and p.mouse_x > (2*i+1)*p.width/8 and p.mouse_x < (2*i+1)*p.width/8+32 and p.mouse_y > 110 and p.mouse_y < 158 and self.clock%4 == 0:
                        new_char = self.characters[(self.characters.index(self.selected_characters[i]) + 1)%len(self.characters)]
                        while new_char in self.selected_characters:
                            new_char = self.characters[(self.characters.index(new_char) + 1)%len(self.characters)]
                        self.selected_characters[i] = new_char

                if p.btn(p.MOUSE_BUTTON_LEFT) and p.mouse_x > p.width/2-24 and p.mouse_x < p.width/2+24 and p.mouse_y > p.height/2 and p.mouse_y < p.height/2+16:
                    self.game_start = True
                    self.menu += 1
                    for i in range(self.nb_player):
                        self.selected_characters[i].player = f'Player{i+1}'
                    self.characters = self.selected_characters
                    for i in range(len(self.characters)):
                        self.characters[i].set_spawn(self.map.starting_points[i], p.width)
 

    def draw(self):
        if self.game_start:
            p.mouse(False)
            p.cls(6)
            p.bltm(0, 0, self.map.tilemap, 0, 0, p.width, p.height, 2)
            for character in self.characters:
                p.blt(character.hitbox.x, character.hitbox.y, 0, character.sprites[character.direction][0], character.sprites[character.direction][1], character.sprites[character.direction][2], character.sprites[character.direction][3], 2)
            for character in self.characters:
                if character.last_punch:
                    p.blt(character.last_punch.x, character.last_punch.y, 0, character.sprites[2][0]+character.punch_frame*16, character.sprites[2][1], character.sprites[2][2], character.sprites[2][3], 2)
        else:
            p.mouse(True)
            if self.menu == 0:
                p.cls(5)
                p.blt(p.width/2-88, p.height/2-16, 1, 0, 16, 176, 32, 2)
            if self.menu == 1:
                p.cls(5)
                p.text(p.width/2-15, 55, f'Player nb: {self.nb_player}', 0)
                p.blt(p.width/2-50, 50, 1, 16, 0, 16, 16, 2)
                p.blt(p.width/2+50, 50, 1, 0, 0, 16, 16, 2)
                for i in range(self.nb_player):
                    p.text((2*i+1)*p.width/8, 90, f'Player{i+1}:', 0)
                    p.blt((2*i+1)*p.width/8, 110, 0, self.selected_characters[i].sprites[0][0], self.selected_characters[i].sprites[0][1], self.selected_characters[i].sprites[0][2], self.selected_characters[i].sprites[0][3], 2)
                p.text(p.width/2-15, p.height/2, 'Press to start', 0)
                
            if self.menu == 2:
                p.cls(7)
                p.text(p.width/2, p.height/2, f'{self.characters[0].name} win!', 0)



# Exemple of the game with a map and some characters
if __name__=='__main__':
    Game(map1, characters)