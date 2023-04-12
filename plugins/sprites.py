from os import listdir
from random import randint, choice
from pyglet.window import key, mouse
from cocos.layer import Layer
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

    def __init__(self, scroller:ScrollingManager):
        super().__init__()
        self.spr = Sprite('source/gg.png')

        self.spr.position = 400, 360
        self.spr.velocity = 0, 0

        mover = Mover()

        mover.scroller = scroller

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