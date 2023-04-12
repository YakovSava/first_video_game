from cocos.director import director
from cocos.scene import Scene
from cocos.layer import ScrollingManager
from plugins.layers import all_layer
from plugins.background import BackgroundLayer
from plugins.sprites import keyboard

if __name__ == "__main__":
    director.init(
        width=1280,
        height=720,
        caption="Game name"
    )
    director.window.pop_handlers()
    director.window.push_handlers(keyboard)
    scroller = ScrollingManager()

    for layer in all_layer:
        scroller.add(layer)

    for layer in (BackgroundLayer().layers):
        scroller.add(layer)

    scene = Scene()
    scene.add(scroller)

    director.run(scene)