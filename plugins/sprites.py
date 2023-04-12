from os import listdir
from random import randint, choice
from typing import Callable
from pyglet.window import key, mouse
from cocos.director import director
from cocos.layer import Layer, ColorLayer
from cocos.text import Label
from cocos.sprite import Sprite
from cocos.action import Move
from cocos.layer import ScrollingManager

keyboard = key.KeyStateHandler()

class Mover(Move):

    def __init__(self, dt):
        super().step(dt)
        vel_x = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 500
        vel_y = (keyboard[key.UP] - keyboard[key.DOWN]) * 500

        dx, dy = vel_x + dt, vel_y + dt

        last = self.target.get_rect()

        new = last.copy()

        new.x += dx
        new.y += dy

        self.target.velocity = self.target.collide_map(last, new, vel_x, vel_y)
        self.target.position = new.center
        self.scroller.set_focus(*new.center)





class MainHeroSprite(Layer):

    is_event_handler = True

    def __init__(self, scroller:ScrollingManager, collision_handler:Callable):
        super().__init__()
        self.spr = Sprite('source/gg.png')

        self.spr.position = 400, 360
        self.spr.velocity = 0, 0

        mover = Mover()
        mover.scroller = scroller

        self.spr.collide_map = collision_handler

        self.spr.do(mover)

        self.add(self.spr)

    def main_hero_click(self, x ,y) -> bool:
        return (x < self.spr.x + self.spr.width) and (x > self.spr.x) and (y < self.spr.y + self.spr.weight) and (y > self.spr.y)

    def on_mouse_press(self, x, y, button, modifier):
        if button & mouse.LEFT:
            if self.main_hero_click(x, y):
                pass # Open inventory

class NPC(Layer):
    def __init__(self):
        super().__init__()
        self.spr = Sprite(choice(listdir('source/npc/')))

        self.spr.position = 400, 360
        self.spr.velocity = 0, 0

        self.add(self.spr)

    def npc_click(self, x ,y) -> bool:
        return (x < self.spr.x + self.spr.width) and (x > self.spr.x) and (y < self.spr.y + self.spr.weight) and (y > self.spr.y)

    def on_mouse_press(self, x, y, button, modifier):
        if button & mouse.LEFT:
            if self.npc_click(x, y):
                pass # Say random phrase

class DirectedByRobertVeide(ColorLayer):

    def __init__(self):
        super().__init__(*[255 for _ in range(4)])

        self.add_title('Credits', 300)
        self.add_label('Developed by:', 255)
        self.add_label('Savelev Yakov', 150)
        self.add_label('YakovSava', 150)
        self.add_label('Jacob Savelev', 150)
        self.add_label('Denis Ponomarev', 150)

        self.add_title('Special thanks:', 250)
        self.add_label('AtiByte', 150)
        self.add_label('Nastya Sergienko', 150)
        self.add_label('Igor Gygabyte', 150)
        self.add_label('Ryan Gosling', 150)
        self.add_label('JSON Stathem', 150)
        self.add_label('Iosif Stalin', 150)
        self.add_label('Pablo Escobar', 150)
        self.add_label('Kurt Cobein', 150)
        self.add_label('Mark Solarezzof', 150)
        self.add_label('Misha Fifanov', 150)
        self.add_label('Georgy Vorob\'ov', 150)
        self.add_label('Kirill Chornyi', 150)
        self.add_label('Pastuhova Nadezhda', 150)
        self.add_label('Maksim Sidorov', 150)

    def add_title(self, title, y) -> None:
        self.add(Label(
            text=title,
            font_name='Arial',
            font_size=48,
            color=(0, 0, 0, 255),
            anchor_x='center',
            anchor_y='center',
            position=(director.get_window_size()[0] / 2, y)
        ))

    def add_label(self, text, y) -> None:
        self.add(Label(
            text=text,
            font_name='Arial',
            font_size=24,
            color=(0, 0, 0, 255),
            anchor_x='center',
            anchor_y='center',
            position=(director.get_window_size()[0] / 2, y)
        ))