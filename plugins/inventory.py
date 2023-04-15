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
                inventory.write(_encode('[]'))
        if not exists('quests.list'):
            with open('quests.list', 'w', encoding='utf-8') as file:
                file.write(_encode('[]'))
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
        print(_perfecto(self._read_inv(), self._read_quests()))
        self.label.element.text = _perfecto(self._read_inv(), self._read_quests())

    def add_quest(self, quest_title:str) -> None:
        _list = self._read_quests()
        _list.append(quest_title)
        self._write_quests(_list)

    def delete_quest(self, quest_name:str) -> None:
        _list = self._read_quests()
        _list.remove(quest_name)
        self._write_quests(_list)

    def add_item(self, item_name:str) -> None:
        _list = self._read_inv()
        _list.append(item_name)
        self._write_inv(_list)

    def delete_item(self, item_name: str) -> None:
        _list = self._read_inv()
        _list.remove(item_name)
        self._write_inv(_list)