from cocos.layer import ScrollableLayer
from cocos.tiles import load
from cocos.sprite import Sprite

class BackgroundLayer(ScrollableLayer):

    def __init__(self):
        super().__init__()

        background = load('source/map.tmx')
        self.layers = background['ground'], background['deco'], background['trees']
        self.colliders = background['collide']

        self.add(background)

class BackgroundMenulayer(ScrollableLayer):
    def __init__(self):
        super().__init__()
        self.add(Sprite('source/map.png'))

    def is_inside_box(self, *args) -> bool:
        return False