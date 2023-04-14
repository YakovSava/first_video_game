from os import mkdir
from os.path import isdir, join
from json import loads, dumps
from base64 import b64encode, b64decode

def _encode(string:str) -> str:
    return b64encode(bytes(string, 'utf-8')).decode('utf-8')

def _decode(string:str) -> str:
    return b64decode(bytes(string, 'utf-8')).decode('utf-8')

class Saver:
    '''
    Save object (JSON):
    {
        'location': 0,
        'inventory': ['beer', 'beer', 'beer'],
        'quests': ['quest 1', 'quest 2', 'quest 3']
    }
    '''

    def __init__(self, path:str='/saves'):
        if not isdir(path):
            mkdir(path)
        self.path = path

    def read(self, save_name:str='save-1.pgsave') -> dict:
        with open(join(self.path, save_name), 'r', encoding='utf-8') as file:
            return loads(_decode(file.read()))

    def write(self, save_name:str='save-1.pgsave', data:dict='{}') -> None:
        with open(join(self.path, save_name), 'w', encoding='utf-8') as file:
            file.write(_encode(dumps(data)))