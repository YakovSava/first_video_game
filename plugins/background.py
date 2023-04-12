from cocos.layer import ScrollableLayer
from cocos.sprite import Sprite
from cocos.tiles import load

class BackgroundLayer(ScrollableLayer):

    def __init__(self):
        super().__init__()

        background = load('source/map.tmx')
        self.layers = background['ground'], background['deco'], background['trees']

        self.add(background)

