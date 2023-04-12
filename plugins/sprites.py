from pyglet.window import key, mouse
from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.action import Move

keyboard = key.KeyStateHandler()

class Mover(Move):

    def __init__(self, dt):
        super().step(dt)
        vel_x = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 500
        vel_y = (keyboard[key.UP] - keyboard[key.DOWN]) * 500

        self.target.velocity = vel_x, vel_y

class MainHeroSprite(Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()
        self.spr = Sprite('source/gg.png')

        self.spr.position = 400, 360
        self.spr.velocity = 0, 0

        self.spr.do(Mover())

        self.add(self.spr)

    def main_hero_click(self, x ,y) -> bool:
        return (x < self.spr.x + self.spr.width) and (x > self.spr.x) and (y < self.spr.y + self.spr.weight) and (y > self.spr.y)

    def on_mouse_press(self, x, y, button, modifier):
        if button & mouse.LEFT:
            if self.main_hero_click(x, y):
                pass