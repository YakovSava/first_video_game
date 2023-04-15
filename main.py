from cocos.menu import Menu, MenuItem, shake, shake_back
from cocos.mapcolliders import TmxObjectMapCollider, make_collision_handler
from cocos.director import director
from cocos.scene import Scene
from cocos.layer import ScrollingManager
from plugins.sprites import MainHeroSprite, DirectedByRobertVeide, npc_layers
from plugins.background import BackgroundLayer, BackgroundMenulayer
from plugins.sprites import keyboard
from local import get, get_all_langs, set_lang

lang = get()

class LangMenu(Menu):
    _handlers_enabled = False

    def __init__(self):
        super().__init__(lang['game_name_langs'])

        items = [
            MenuItem(message, self.set_lang, message)
            for message in (get_all_langs())
        ]
        self.create_menu(items, shake(), shake_back())

    def set_lang(self, lang:str) -> None:
        set_lang(lang)
        director.window.close()

class MainMenu(Menu):
    _handlers_enabled = False

    def __init__(self):
        super().__init__(lang['game_name'])

        items = [
            MenuItem(message, action)
            for message, action in [
                [lang['new_game'], self.new_game],
                [lang['devs'], self.developers],
                [lang['langs'], self.change_lang],
                [lang['exit'], director.window.close]
            ]
        ]
        self.create_menu(items, shake(), shake_back())

        # mmbg = BackgroundMenulayer()
        # mmbg.position = tuple(map(lambda x: x / 2, director.get_window_size()))
        # self.add(mmbg)

    def new_game(self) -> None:
        director.window.pop_handlers()
        director.window.push_handlers(keyboard)

        background = BackgroundLayer()

        mapcollider = TmxObjectMapCollider()
        mapcollider.on_bump_handler = mapcollider.on_bump_bounce
        collision_handler = make_collision_handler(mapcollider, background.colliders)

        scroller = ScrollingManager()

        mh = MainHeroSprite(scroller, collision_handler, DirectedByRobertVeide)
        scene = Scene()


        for layer in (background.layers):
            scroller.add(layer)

        for layer in npc_layers:
            scroller.add(layer)

        scroller.add(mh)

        scene.add(scroller)

        director.run(scene)

    def change_lang(self) -> None:
        lang_menu = LangMenu()

        director.run(lang_menu)

    def developers(self) -> None:
        title = DirectedByRobertVeide()

        director.run(title)

if __name__ == "__main__":
    w = director.init(
        width=960,
        height=640,
        caption=lang['game_name']
    )
    director.window = w
    menu = MainMenu()

    director.run(menu)