from cocos.layer import ScrollableLayer, Layer
from cocos.sprite import Sprite
from cocos.tiles import load
from cocos.menu import Menu, MenuItem
from plugins.inventory import Inventory

class Button(Layer):

    def __init__(self):
        super().__init__()
        button_image = Sprite('source/freemasonry.png')
        button = MenuItem('Notebook', self.on_button_click)
        menu = Menu(button)
        menu.position = button_image.width // 2, button_image.height // 2

        self.add(button_image)
        self.add(menu)

    def on_button_click(self) -> None:
        inv = Inventory()
        self.add(inv)

class BackgroundLayer(ScrollableLayer):

    def __init__(self):
        super().__init__()

        background = load('source/map.tmx')
        self.layers = background['ground'], background['deco'], background['trees']
        self.colliders = background['collide']

        self.add(background)
        self.add(Button())