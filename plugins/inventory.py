from os.path import exists
from base64 import b64encode, b64decode

def _encode(string:str) -> str:
    return b64encode(bytes(string, 'utf-8')).decode('utf-8')

def _decode(string:str) -> str:
    return b64decode(bytes(string, 'utf-8')).decode('utf-8')

class Inventory():

    def __init__(self):
        if not exists('inventory.list'):
            with open('inventory.list', 'w', encoding='utf-8') as inventory:
                inventory.write(str(
                    [
                        _encode(string)
                        for string in ['0' for i in range(5)]
                    ]
                ))

    def _read(self) -> str:
        with open('inventory.list', 'r', encoding='utf-8') as file:
            return file.read()

    def _write(self, _list:list) -> None:
        with open('inventory.list', 'w', encoding='utf-8') as file:
            file.write(str(
                list(map(
                    _decode,
                    _list
                ))
            ))