from pyglet.window import key
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

    def __init__(self):
        super().__init__()
        spr = Sprite('source/gg.png')

        spr.position = 400, 360
        spr.velocity = 0, 0

        spr.do(Mover())

        self.add(spr)