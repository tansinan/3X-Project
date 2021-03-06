import cocos
from cocos.sprite import Sprite
from cocos.director import director
from cocos.actions import MoveTo, Delay, sequence
from global_vars import Main as Global
from data_loader import Main as Data
from terrain_container import Main as Terrain_Container
from person_container import Main as Person_Container
import map_controller
from utility import *
import pyglet

def test_print(self):
    print('hello')


class Arena(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        pyglet.resource.path = ['../img']
        pyglet.resource.reindex()
        self.size = 80
        self.select = (0, 0)
        self.origin_color = WHITE
        data = Data()
        global_vars = Global(data)
        terrain_container_test = Terrain_Container(data.terrain_map, global_vars.terrainBank)
        person_container_test = Person_Container(data.map_armylist, global_vars.personBank)
        map1 = map_controller.Main(terrain_container_test, person_container_test, global_vars)
        self.w = terrain_container_test.M
        self.h = terrain_container_test.N

        super(Arena, self).__init__(r=0,g=0,b=0,a=255,width=self.w*self.size,height=self.h*self.size)
        self.tiles = []
        for x in range(self.w):
            tl_x = []
            for y in range(self.h):
                tile = Tile(pos=coordinate(x, y, self.size), size=self.size)
                self.add(tile)
                tl_x.append(tile)
            self.tiles.append(tl_x)

        self.repaint(map1)
        self.map = map1
        self.text = cocos.text.RichLabel('ROUND 1' ,
                                     font_name='times new roman',
                                     font_size=36,
                                     position=(0, 420),
                                    color = (127, 255, 170, 255))
        self.add(self.text)
        self.end_turn = Sprite(image='ring.png', position=(560,200), color=MAROON, scale=0.8)

        self.add(self.end_turn)
        self.add(cocos.text.RichLabel(text='END', position=(520, 190), font_size=30))

        self.next_round()

    def move(self, id, i, j):
        obj = self.person[id]
        mov = MoveTo(coordinate(i, j, self.size), 2)
        obj.do(Delay(0.5)+ mov + cocos.actions.CallFunc(self.take_turn))


    def take_turn(self): #according to the controller, take turn of next charactor
        map = self.map
        if map.controller == 0:
            map.player_turn(self)
        else:
            map.ai_turn(self)

    def next_round(self):
        self.map.turn += 1
        self.text.element.text = 'ROUND '+str(self.map.turn)
        if self.map.turn > 6 :
            director.pop()
        else:
            print('enemy phase')
            self.take_turn()




    def repaint(self, map_controller):
        position = map_controller.person_container.position
        controller = map_controller.person_container.controller
        self.person = {}
        for id in position:
            (x, y) = position[id]
            if controller[id] == 1 :
                color = ORANGE
            else:
                color = SKY_BLUE
            self.person[id] = Ally(pos=coordinate(x, y, self.size), color=color, size=self.size)
            self.add(self.person[id])


    def on_mouse_motion(self, x, y, buttons, modifiers):
        i, j = coordinate_t(x, y, self.size)
        if (x-560)**2 + (y-200)**2 < 80**2:
            self.end_turn.color = GOLD
        else:
            self.end_turn.color = MAROON
        if i in range(0, self.w) and j in range(0, self.h):
            i0, j0 = self.select
            self.tiles[i0][j0].color = self.origin_color
            self.origin_color = self.tiles[i][j].color
            self.tiles[i][j].color = LIGHT_PINK
            self.select = i, j


    def on_mouse_press(self, x, y, buttons, modifiers):
        i, j = coordinate_t(x, y, self.size)
        map = self.map
        if self.end_turn.color == list(GOLD):
            map.controller = 1
            map.reset_state(0)
            self.next_round()
        else:
            if i in range(0, self.w) and j in range(0, self.h):
                if map.person_container.movable['1']:
                    map.person_container.position['1'] = i, j
                    map.person_container.movable['1'] = False
                    self.move('1', i, j)






class Tile(Sprite):
    def __init__(self, size=50,pos=None):
        path = 'ring.png'
        super(Tile, self).__init__(image=path)
        self.scale = size/self.height
        self.color = (255, 255, 255)
        self.position = pos

class Ally(Sprite):
    def __init__(self, size=50,pos=None, color=(135, 206, 235)):
        path = 'ring.png'
        super(Ally, self).__init__(image=path)
        self.scale = size/self.height * 0.8
        self.color = color
        self.position = pos

    def on_enter(self):
        super(Ally, self).on_enter()
        director.window.push_handlers(self.on_mouse_press)

    def on_exit(self):
        director.window.pop_handlers(self.on_mouse_press)

    def on_mouse_press(self, x, y, buttons, modfiers):
        pass

class Check_state(Delay):
    def start(self):
        arena = self.target.parent     #type:Arena
        map = arena.map
        map.turn += 1
        if map.turn <= 5:
            if map.check_states():
                self.target.do(sequence(MoveTo(coordinate(map.i, map.j, arena.size), 2), Check_state(1)))
            else:
                self.target.do(Check_state(1))
        else:
            print('gg')



    def stop(self):
        arena = self.target     #type:Arena
        arena.is_event_handler = True



if __name__ == '__main__':
    director.init(caption='3X-Project')
    director.run(cocos.scene.Scene(Arena()))
