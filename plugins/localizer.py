from os import mkdir
from os.path import isdir, join
from random import choice
from json import loads

class Localizer:
    '''
    Please use a three-letter language designation for the ISO-639 file name.
    '''


    def __init__(self, path:str='local'):
        if not isdir(path):
            mkdir(path)
        self.path = path

    def get(self, local:str='eng') -> dict:
        with open(join(self.path, local), 'r', encoding='utf-8') as file:
            return loads(file.read())

    def get_phrase(self, local:str='eng') -> str:
        return choice(self.get(local=local)['phrazes'])