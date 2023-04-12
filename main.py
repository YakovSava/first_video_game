from cocos.menu import Menu, MenuItem, shake, shake_back
from cocos.mapcolliders import TmxObjectMapCollider, make_collision_handler
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import ScrollingManager
from plugins.sprites import npc_layer, MainHeroSprite
from plugins.background import BackgroundLayer
from plugins.sprites import keyboard

class MainMenu(Menu):

    def __init__(self):
        super().__init__("Game name")

        items = [
            MenuItem(message)
            for message, action in [
                ['New game', self.new_game],
                ['Developers', self.developers],
                ['Exit', director.window.close]
            ]
        ]

        self.create_menu(items, shake(), shake_back())

    def new_game(self) -> None:
        director.window.pop_handlers()
        director.window.push_handlers(keyboard)

        background = BackgroundLayer()

        mapcollider = TmxObjectMapCollider()
        mapcollider.on_bump_handler = mapcollider.on_bump_bounce
        collision_handler = make_collision_handler(mapcollider, background.colliders)

        scroller = ScrollingManager()

        mh = MainHeroSprite(scroller, collision_handler)

        for layer in npc_layer:
            scroller.add(layer)

        for layer in (background.layers):
            scroller.add(layer)

        scene = Scene()
        scene.add(scroller)

        director.run()

    def developers(self) -> None:
        pass

if __name__ == "__main__":
    director.init(
        width=1280,
        height=720,
        caption="Game name"
    )
    menu = MainMenu()

    director.run(menu)