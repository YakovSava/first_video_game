from cocos.menu import Menu, MenuItem, shake, shake_back
from cocos.mapcolliders import TmxObjectMapCollider, make_collision_handler
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import ScrollingManager
from plugins.sprites import npc_layers, MainHeroSprite, DirectedByRobertVeide
from plugins.background import BackgroundLayer, Button
from plugins.sprites import keyboard

class MainMenu(Menu):
    _handlers_enabled = False

    def __init__(self):
        super().__init__("Game name")

        items = [
            MenuItem(message, action)
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

        mh = MainHeroSprite(scroller, collision_handler, DirectedByRobertVeide)

        for layer in npc_layers:
            scroller.add(layer)

        for layer in (background.layers):
            scroller.add(layer)

        scroller.add(mh)
        scroller.add(background.colliders)

        scene = Scene()
        scene.add(scroller)

        director.run(scene)

    def developers(self) -> None:
        title = DirectedByRobertVeide()

        director.run(title)

if __name__ == "__main__":
    w = director.init(
        width=960,
        height=640,
        caption="Game name",
        autoscale=True
    )
    director.window = w
    menu = MainMenu()

    director.run(menu)