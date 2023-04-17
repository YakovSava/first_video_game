from os import listdir
from time import sleep
from threading import Timer
from tkinter.messagebox import showinfo
from random import choice, randint
from typing import Callable, Iterator
from pyglet.window import key, mouse
from cocos.director import director
from cocos.layer import ColorLayer, ScrollableLayer
from cocos.text import Label
from cocos.sprite import Sprite
from cocos.actions import Move
from cocos.layer import ScrollingManager
from plugins.inventory import Inventory
from local import get

lang = get()

keyboard = key.KeyStateHandler()

def _timer(interval:int, function:Callable, args:tuple=tuple(), kwargs:dict={}) -> None:

    Timer(interval, function, args=args, kwargs=kwargs)

class DialogMenu(ScrollableLayer):

    def __init__(self, x:int, y:int):
        super().__init__()
        self.label = Label(
            text=choice(lang['phrazes']),
            font_size=14,
            color=(0, 0, 0, 255),
            anchor_x='center',
            anchor_y='center',
            position=(x-4, y+23)
        )
        self.add(self.label)
        t = _timer(3, self.change_visibility)

    def change_visibility(self) -> None:
        self.label.visible = False
        self.visible = False

    def open(self, x, y) -> None:
        self.label.element.text = choice(lang['phrazes'])
        self.label.visible = True
        self.visible = True
        t = _timer(3, self.change_visibility)

class Mover(Move):

    def __init__(self, t):
        super().__init__()
        self.t = t

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
            self.target.teleport_to_location(self.t)


class _MainHeroSprite(Sprite):

    def teleport_to_location(self, t, *args) -> None:
        director.run(t(*args))

class MainHeroSprite(ScrollableLayer):

    is_event_handler = True

    def __init__(self, scroller:ScrollingManager, collision_handler:Callable, t, *args):
        super().__init__()
        self.spr = _MainHeroSprite('source/gg.png')

        self.spr.position = 79, 616
        self.spr.velocity = 0, 0

        mover = Mover(t, *args)
        mover.scroller = scroller

        self.spr.collide_map = collision_handler

        self.spr.do(mover)

        self.add(self.spr)

        self.inv = Inventory()
        self.inv.visible = False
        self.add(self.inv)

    def main_hero_click(self, x, y) -> bool:
        return (x < self.spr.x + self.spr.width) and (x > self.spr.x) and (y < self.spr.y + self.spr.width) and (y > self.spr.y)

    def on_mouse_press(self, x, y, button, modifier):
        print(x, y)
        if button & mouse.LEFT:
            if self.main_hero_click(x, y):
                if not self.inv.visible:
                    self.inv.change()
                    self.inv.visible = True
        if button & mouse.RIGHT:
            if self.inv.visible:
                self.inv.visible = False

class DirectedByRobertVeide(ColorLayer):
    _handlers_enabled = False

    def __init__(self):
        super().__init__(*[255 for _ in range(4)])

        self.add_title(lang['credits'], 540)
        self.add_label(lang['devs_devs'], 510)
        self.add_label(lang['sy'], 490)
        self.add_label(lang['ys'], 470)
        self.add_label(lang['js'], 450)
        self.add_label(lang['dp'], 430)

        self.add_title(lang['special'], 400)
        self.add_label('AtiByte', 360)
        self.add_label(lang['ns'], 340)
        self.add_label(lang['ig'], 320)
        self.add_label(lang['rg'], 300)
        self.add_label(lang['json_s'], 280)
        self.add_label(lang['is'], 260)
        self.add_label(lang['pe'], 240)
        self.add_label(lang['kc'], 220)
        self.add_label(lang['mark'], 200)
        self.add_label(lang['misha'], 180)
        self.add_label(lang['georgy'], 160)
        self.add_label(lang['kiril'], 140)
        self.add_label(lang['pon'], 120)
        self.add_label(lang['ms'], 100)

        showinfo(lang['game_name'], lang['thanks'])

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

class NPC(ScrollableLayer):
    is_event_handler = True

    def __init__(self):
        super().__init__()

        self.spr = Sprite(f'source/npc/{choice(listdir("source/npc/"))}')
        self.spr.position = randint(230, 520), randint(120, 840)

        self.add(self.spr)

    def npc_click(self, x, y) -> bool:
        return bool((x < self.spr.x + self.spr.width) and (x > self.spr.x) and (y < self.spr.y + self.spr.width) and (
                    y > self.spr.y))
    def on_mouse_press(self, x, y, button, modifier):
        if button & mouse.LEFT:
            if self.npc_click(x, y):
                if hasattr(self, 'dialog'):
                    self.dialog.open(x, y)
                else:
                    self.dialog = DialogMenu(x, y)
                    self.add(self.dialog)

class NPCQuest(ScrollableLayer):
    is_event_handler = True

    class DialogMenu(ScrollableLayer):

        def __init__(self, x: int, y: int, main_hero:MainHeroSprite):
            super().__init__(parallax=1)
            self.quest = choice(lang['quests'])
            self.quest_complete = False
            self.replica = True
            self.label = Label(
                text=self.quest['dialog'][0],
                font_size=14,
                color=(0, 0, 0, 255),
                anchor_x='center',
                anchor_y='center',
                position=(x - 4, y + 23)
            )
            self.mh = main_hero
            self.add(self.label)

        def _iterator(self) -> Iterator:
            for quest in self.quest['dialog'][1:]:
                yield quest

        def step(self) -> None:
            if self.replica:
                for text in self._iterator():
                    setattr(self.label.element, 'text', text)
                    sleep(2)
                self.replica = False
                _timer(3, self.change_visibility)
            else:
                if self.quest_complete:
                    self.label.element.text = self.quest['thanks']
                else:
                    self.label.element.text = self.quest['help']
                _timer(3, self.change_visibility)

        def change_visibility(self) -> None:
            self.label.visible = False
            self.visible = False


    def __init__(self, mh:MainHeroSprite):
        super().__init__()

        self.spr = Sprite(f'source/npc/{choice(listdir("source/npc/"))}')
        self.spr.position = randint(230, 520), randint(120, 840)

        self.mh = mh

        self.add(self.spr)

    def npc_click(self, x, y) -> bool:
        return bool((x < self.spr.x + self.spr.width) and (x > self.spr.x) and (y < self.spr.y + self.spr.width) and (
                    y > self.spr.y))
    def on_mouse_press(self, x, y, button, modifier):
        if button & mouse.LEFT:
            if self.npc_click(x, y):
                if not hasattr(self, 'dialog'):
                    self.dialog = self.DialogMenu(x, y, self.mh)
                    self.dialog.step()
                    self.add(self.dialog)

npc_layers = [
    NPC()
    for _ in range(6)
]

quest_npcs = [
    NPCQuest
    for _ in range(2)
]