from os import listdir
from os.path import join
from toml import loads

def _get_lang() -> str:
    with open('local/config.toml', 'r', encoding='utf-8') as file:
        return loads(file.read())['lang']

def get(name:str=_get_lang()) -> dict:
    with open(join('local/langs', f'{name}.lang'), 'r', encoding='utf-8') as file:
        return loads(file.read())

def set_lang(name:str) -> None:
    with open('local/config.toml', 'w', encoding='utf-8') as file:
        file.write(f'lang = "{name}"')

def get_all_langs() -> list[str]:
    return list(map(lambda x: x[:-5], listdir('local/langs/')))