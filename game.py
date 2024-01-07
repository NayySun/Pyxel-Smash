from datas import *
import pyxel as p
import json, random



class Game:
    def __init__(self, map: Map, characters: Character):
        p.init(SCREEN_LENGTH, SCREEN_HEIGHT, 'Game', 60)
        self.game_start = False
        self.menu = 0
        self.nb_player = 2

        self.map = map
        self.clock = 0
        self.pattern = [[1 if not random.randint(0, 39) and j < p.height/2 else 0 for j in range(int(p.height/16))] for i in range(int(p.width/16))]
        with open('mapping.json', 'r') as file:
            self.mapping = json.load(file)
        self.characters = characters
        for i in range(len(self.characters)):
            self.characters[i].set_spawn(self.map.starting_points[i], p.width)
        
        p.load('ressources.pyxres')
        p.run(self.update, self.draw)

    def update(self):
        if self.game_start:
            i = 0
            for character in self.characters:
                self.clock += 1
                i += 1
                if p.btn(eval(f'p.{self.mapping[character.name]["right"]}')):
                    character.move_right(self.map.objects)
                if p.btn(eval(f'p.{self.mapping[character.name]["left"]}')):
                    character.move_left(self.map.objects)
                if p.btn(eval(f'p.{self.mapping[character.name]["up"]}')):
                    character.move_up()
                if p.btn(eval(f'p.{self.mapping[character.name]["down"]}')):
                    character.move_down()
                character.fall(self.map.objects, p.height)
                if p.btn(eval(f'p.{self.mapping[character.name]["attack"]}')) and character.is_punching == False and character.on_wall == False:
                    character.punch(self.characters)
                if p.btnr(eval(f'p.{self.mapping[character.name]["attack"]}')):
                    character.is_punching = False
            if len(self.characters) == 1:
                self.game_start = False    
        else:
            self.clock += 1
            if self.menu == 0:
                if p.btn(p.MOUSE_BUTTON_LEFT):
                    self.menu += 1
            if self.menu == 1:
                if p.btn(p.MOUSE_BUTTON_LEFT) and p.mouse_x > p.width/2-40 and p.mouse_x < p.width/2-24 and p.mouse_y > p.height/2-50 and p.mouse_y < p.height/2-4 and self.nb_player > 2 and self.clock%4 == 0:
                    self.nb_player -= 1
                if p.btn(p.MOUSE_BUTTON_LEFT) and p.mouse_x > p.width/2-8 and p.mouse_x < p.width/2+8 and p.mouse_y > p.height/2-50 and p.mouse_y < p.height/2-4 and self.nb_player < 4 and self.clock%4 == 0:
                    self.nb_player += 1   
                if p.btn(p.MOUSE_BUTTON_LEFT) and p.mouse_x > p.width/2-24 and p.mouse_x < p.width/2+24 and p.mouse_y > p.height/2 and p.mouse_y < p.height/2+16:
                    for i in range(len(characters)-self.nb_player):
                        self.characters.pop(-1)
                    self.game_start = True
                    self.menu += 1

    def draw(self):
        if self.game_start:
            p.mouse(False)
            p.cls(6)
            for i in range(int(p.width/16)):
                for j in range(int(p.height/16)):
                    if self.pattern[i][j]:
                        p.blt((32*i+self.clock)%p.width, 32*j, 0, 48, 128, 16, 16, 13)
            p.bltm(0, 0, 0, 0, 0, p.width, p.height, 13)
            for character in self.characters:
                p.blt(character.hitbox.x, character.hitbox.y, 0, character.sprites[character.direction][0], character.sprites[character.direction][1], character.sprites[character.direction][2], character.sprites[character.direction][3], 13)
            for character in self.characters:
                if character.punch_cooldown:
                    character.punch_cooldown -= 1
                    p.blt(character.last_punch.x, character.last_punch.y, 0, character.sprites[2][0], character.sprites[2][1], character.sprites[2][2], character.sprites[2][3], 13)
        else:
            p.mouse(True)
            if self.menu == 0:
                p.cls(5)
                p.blt(p.width/2-72, p.height/2-100, 1, 0, 0, 144, 32, 13)
                p.blt(p.width/2-52, p.height/2+50, 0, 0, 208, 104, 32, 13)
            if self.menu == 1:
                p.cls(5)
                p.blt(p.width/2-120, p.height/2-50, 1, 0, 32, 80, 16, 13)
                p.blt(p.width/2-40, p.height/2-50, 1, 16, 64, 16, 16, 13)
                p.blt(p.width/2-8, p.height/2-50, 1, 0, 64, 16, 16, 13)
                p.blt(p.width/2-20, p.height/2-50, 1, self.nb_player*8, 48, 8, 16, 13)
                p.blt(p.width/2-24, p.height/2, 1, 0, 80, 48, 16, 13)
            if self.menu == 2:
                p.cls(7)
                p.text(p.width/2, p.height/2, f'{self.characters[0].name} win!', 0)

if __name__=='__main__':
    Game(map1, characters)