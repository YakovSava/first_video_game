from os.path import exists
from base64 import b64encode, b64decode
from cocos.text import Label
from cocos.layer import ColorLayer
from cocos.sprite import Sprite
from cocos.actions import FadeIn, FadeOut

def _encode(string:str) -> str:
    return b64encode(bytes(string, 'utf-8')).decode('utf-8')

def _decode(string:str) -> str:
    return b64decode(bytes(string, 'utf-8')).decode('utf-8')

class Inventory(ColorLayer):

    def __init__(self):
        super().__init__((255, 255, 255, 150), width=640, height=480)
        if not exists('inventory.list'):
            with open('inventory.list', 'w', encoding='utf-8') as inventory:
                inventory.write(str(
                    [
                        _encode(string)
                        for string in ['0' for i in range(5)]
                    ]
                ))
        image = Sprite('source/notebook.jpg')
        image.position = self.width / 2, self.height / 2
        self.add(image)

        label = Label(
            text="\n".join(self._read()),
            font_name='Arial',
            font_size=30,
            anchor_x='center',
            anchor_y='center'
        )
        label.position = self.width / 2, self.height / 2
        self.add(label)

    def on_enter(self) -> None:
        super().on_enter()
        self.opacity = 0
        self.do(FadeIn(0.5))

    def on_exit(self) -> None:
        self.do(FadeOut(0.5))
        super().on_exit()

    def _read(self) -> list[str]:
        with open('inventory.list', 'r', encoding='utf-8') as file:
            return list(map(_decode, eval(file.read())))

    def _write(self, _list:list) -> None:
        with open('inventory.list', 'w', encoding='utf-8') as file:
            file.write(str(
                list(map(
                    _encode,
                    _list
                ))
            ))

