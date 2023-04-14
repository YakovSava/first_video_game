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

def _perfecto(inventory:list, quests:list) -> str:
    end = ""
    end += 'Inventory:\n'
    for item in inventory:
        end += f'- {item}\n'
    end += '\n\nQuests:'
    for quest in quests:
        end += f'- {quest}\n'
    return end

class Inventory(ColorLayer):
    is_event_handler = True

    def __init__(self):
        super().__init__(255, 255, 255, 150, width=640, height=480)
        if not exists('inventory.list'):
            with open('inventory.list', 'w', encoding='utf-8') as inventory:
                inventory.write(_encode(str(['null' for _ in range(5)])))
        if not exists('quests.list'):
            with open('quests.list', 'w', encoding='utf-8') as file:
                file.write(_encode(str(['null' for _ in range(5)])))
        image = Sprite('source/notebook.jpg')
        image.position = self.width / 2, self.height / 2
        self.add(image)

        self.label = Label(
            text=_perfecto(self._read_inv(), self._read_quests()),
            font_name='Arial',
            font_size=30,
            color=(0, 0, 0, 255),
            anchor_x='center',
            anchor_y='center'
        )
        self.label.position = self.width / 2, self.height / 2
        self.add(self.label)

    def _read_inv(self) -> list[str]:
        with open('inventory.list', 'r', encoding='utf-8') as file:
            return eval(_decode(file.read()))

    def _write_inv(self, _list:list) -> None:
        with open('inventory.list', 'w', encoding='utf-8') as file:
            file.write(_encode(str(_list)))

    def _read_quests(self) -> list[str]:
        with open('quests.list', 'r', encoding='utf-8') as file:
            return eval(_decode(file.read()))

    def _write_quests(self, _list:list) -> None:
        with open('quests.list', 'w', encoding='utf-8') as file:
            file.write(_encode(str(_list)))

    def change(self) -> None:
        self.label.element.text = _perfecto(self._read_inv(), self._read_quests())