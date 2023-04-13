from os import listdir
from random import choice
from typing import Callable
from pyglet.window import key, mouse
from cocos.director import director
from cocos.layer import Layer, ColorLayer, ScrollableLayer
from cocos.text import Label
from cocos.sprite import Sprite
from cocos.actions import Move, MoveTo
from cocos.layer import ScrollingManager
from plugins.inventory import Inventory

keyboard = key.KeyStateHandler()

def _all(iterable) -> bool:
    logic = False
    for l in iterable:
        logic = logic and l
    return logic

class Mover(Move):

    def step(self, dt):
        super().step(dt)
        vel_x = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 5
        vel_y = (keyboard[key.UP] - keyboard[key.DOWN]) * 5

        dx, dy = vel_x + dt, vel_y + dt

        last = self.target.get_rect()

        new = last.copy()

        new.x += dx
        new.y += dy

        self.target.velocity = self.target.collide_map(last, new, vel_x, vel_y)
        self.target.position = new.center
        self.scroller.set_focus(*new.center)

        x, y = list(map(lambda x: int(round(x, 0)), self.target.position))

        if (x in range(55, 104)) and (y in range(0, 16)):
            self.target.teleport_to_location()


class _MainHeroSprite(Sprite):

    def teleport_to_location(self) -> None:
        print('Teleport!')

class MainHeroSprite(ScrollableLayer):

    is_event_handler = True

    def __init__(self, scroller:ScrollingManager, collision_handler:Callable):
        super().__init__()
        self.spr = _MainHeroSprite('source/gg.png')

        self.spr.position = 79, 616
        self.spr.velocity = 0, 0

        mover = Mover()
        mover.scroller = scroller

        self.spr.collide_map = collision_handler

        self.spr.do(mover)

        self.add(self.spr)

        self.sprite_action = MoveTo((0, 0), duration=5)

        self.inventory = False

    def main_hero_click(self, x ,y) -> bool:
        return (x < self.spr.x + self.spr.width) and (x > self.spr.x) and (y < self.spr.y + self.spr.width) and (y > self.spr.y)

    def on_mouse_press(self, x, y, button, modifier):
        print(x, y)
        if button & mouse.LEFT:
            if self.main_hero_click(x, y):
                if not self.inventory:
                    self.inv = Inventory()
                    self.add(self.inv)
        if hasattr(self, 'inv'):
            self.remove_action(self.inv)

class NPC(Layer):
    def __init__(self):
        super().__init__()
        self.spr = Sprite(choice(listdir('source/npc/')))

        self.spr.position = 400, 360
        self.spr.velocity = 0, 0

        self.add(self.spr)

    def npc_click(self, x ,y) -> bool:
        return (x < self.spr.x + self.spr.width) and (x > self.spr.x) and (y - 4 < self.spr.y + self.spr.weight) and (y - 4 > self.spr.y)

    def on_mouse_press(self, x, y, button, modifier):
        if button & mouse.LEFT:
            if self.npc_click(x, y):
                print('NPC click!')

class DirectedByRobertVeide(ColorLayer):
    _handlers_enabled = False

    def __init__(self):
        super().__init__(*[255 for _ in range(4)])

        self.add_title('Credits', 540)
        self.add_label('Developed by:', 510)
        self.add_label('Savelev Yakov', 490)
        self.add_label('YakovSava', 470)
        self.add_label('Jacob Savelev', 450)
        self.add_label('Denis Ponomarev', 430)

        self.add_title('Special thanks:', 400)
        self.add_label('AtiByte', 360)
        self.add_label('Nastya Sergienko', 340)
        self.add_label('Igor Gygabyte', 320)
        self.add_label('Ryan Gosling', 300)
        self.add_label('JSON Stathem', 280)
        self.add_label('Iosif Stalin', 260)
        self.add_label('Pablo Escobar', 240)
        self.add_label('Kurt Cobein', 220)
        self.add_label('Mark Solarezzof', 200)
        self.add_label('Misha Fifanov', 180)
        self.add_label('Georgy Vorob\'ov', 160)
        self.add_label('Kirill Chornyi', 140)
        self.add_label('Pastuhova Nadezhda', 120)
        self.add_label('Maksim Sidorov', 100)

    def add_title(self, title, y) -> None:
        self.add(Label(
            text=title,
            font_name='Arial',
            font_size=24,
            color=(0, 0, 0, 255),
            anchor_x='center',
            anchor_y='center',
            position=(director.get_window_size()[0] / 2, y)
        ))

    def add_label(self, text, y) -> None:
        self.add(Label(
            text=text,
            font_name='Arial',
            font_size=12,
            color=(0, 0, 0, 255),
            anchor_x='center',
            anchor_y='center',
            position=(director.get_window_size()[0] / 2, y)
        ))

# npc_layers = [
#     NPC()
#     for _ in range(4)
# ]