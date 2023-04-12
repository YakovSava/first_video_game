import cocos

from cocos.director import director

class HelloCocos(cocos.layer.Layer):

    def __init__(self):
        super().__init__()
        label = cocos.text.Label(
            "Hello cocos",
            font_size=32,
            anchor_x="center",
            anchor_y="center"
        )
        label.position = 640, 360
        self.add(label)

if __name__ == "__main__":
    director.init(
        width=1280,
        height=720,
        caption="My cocos window"
    )

    hello_layers = HelloCocos()
    test_scene = cocos.scene.Scene(hello_layers)

    director.run(test_scene)