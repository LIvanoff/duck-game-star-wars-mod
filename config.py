GAME_TITLE : str = "Some crappy game"
EDITOR_TITLE : str = "Level Editor"

CLOCK_TICKSPEED : int = 60

WIDTH = 1920
HEIGHT = 1080

ASSETS_PATH = 'assets/'
LEVELS_PATH = 'levels/'

DEFAULT_TILESIZE = 21

LOCATION = [
    'hangar',
    'hoth',
    'mustafar',
    'bespin',
    'tattoine'
]

ROUNDS = 5

WEAPONS = {
    'dlt-19': {
        'name': 'dlt-19',
        'damage': 100,
        'ammo_num': 3,
        'decay': 1.5,
        'path': 'assets/images/weapons/dlt19.png'
    },
    'e-11': {
        'name': 'e-11',
        'damage': 30,
        'ammo_num': 20,
        'decay': 0.2,
        # 'overheating_time': ,
        'path': 'assets/images/weapons/e11.png'},
    'dl-44': {
        'name': 'dl-44',
        'damage': 50,
        'ammo_num': 10,
        'decay': 0.7,
        'path': 'assets/images/weapons/dl44.png'},
    'sonic imploder': {
        'name': 'sonic imploder',
        'damage': 100,
        'radius': 20,
        'explosion_time': 3.5,
        'path': 'assets/images/weapons/sonic-imploder.png'}
}

# PLAYER PROPS
JUMP_STRENGTH = 2
MAX_JUMPS = 1