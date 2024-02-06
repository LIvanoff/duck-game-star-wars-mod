import pygame

from tile import *
from config import DEFAULT_TILESIZE

import json

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])) : 0,
    tuple(sorted([(1, 0)])) : 1,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])) : 2,
    tuple(sorted([(-1, 0), (0, 1)])) : 3,
    tuple(sorted([(-1, 0)])) : 4,
    tuple(sorted([(-1, 0), (1, 0)])) : 5,
    tuple(sorted([(1, 0), (0, 1), (0, -1)])) : 6,
    tuple(sorted([(1, 0), (0, -1)])) : 7,
    tuple(sorted([(-1, 0), (0, 1), (0, -1)])) : 8,
    tuple(sorted([(0, -1)])) : 9,
    tuple(sorted([(1, 0), (-1, 0), (0, -1), (0, 1)])) : 10,
    tuple(sorted([(1, 0), (-1, 0), (0, -1)])) : 11,
    tuple(sorted([(-1, 0), (0, -1)])) : 12,
}

NEIGHBOR_OFFSETS_COL = [(-1, 0), (-1, 1), (-1, -1), (0, 0), (0, 1), (0, -1), (1, 0), (1, 1), (1, -1)]
COLLIDABLE_TILES = {'crates', 'grass'}

NEIGHBOR_OFFSETS_AUTOTILE = [(1, 0), (-1, 0), (0, -1), (0, 1)]
AUTOTILE_CLAZZS = {'grass'}

class Tilemap:
    def __init__(self, game, tileSize : int = DEFAULT_TILESIZE) -> None:
        self.game = game
        self.tileSize = tileSize
        self.onGridTilemap = {}
        self.offGridTilemap = []

        # self.mockTiles()


    def tilesAround(self, entity):
        tiles = []
        gridPos = (int((entity.pos[0] + entity.size[0]) // self.tileSize), int((entity.pos[1] + entity.size[1]) // self.tileSize))

        for offset in NEIGHBOR_OFFSETS_COL:
            checkLocation = f'{gridPos[0] + offset[0]}:{gridPos[1] + offset[1]}'
            if checkLocation in self.onGridTilemap.keys():
                tiles.append(self.onGridTilemap[checkLocation])

        return tiles
    

    def collisionRects(self, entity):
        rects = []
        for tile in self.tilesAround(entity):
            if tile.clazz in COLLIDABLE_TILES:
                rects.append(pygame.Rect(tile.pos[0] * self.tileSize, tile.pos[1] * self.tileSize, self.tileSize, self.tileSize))

        return rects
    

    def autotile(self):
        for location in self.onGridTilemap:
            tile = self.onGridTilemap[location]
            neighbors = set()
            for shift in NEIGHBOR_OFFSETS_AUTOTILE:
                checkLocation = f'{tile.pos[0] + shift[0]}:{tile.pos[1] + shift[1]}'
                if checkLocation in self.onGridTilemap:
                    if self.onGridTilemap[checkLocation].clazz == tile.clazz:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile.clazz in AUTOTILE_CLAZZS) and (neighbors in AUTOTILE_MAP):
                tile.type = AUTOTILE_MAP[neighbors]


    def save(self, path):
        onGridJsonable = {}
        for k, v in self.onGridTilemap.items():
            onGridJsonable[k] = v.toDict()

        offGridJsonable = list(map(lambda it: it.toDict(), self.offGridTilemap))

        with open(path, 'w') as savefile:
            json.dump(
                {
                    'onGridTilemap'  : onGridJsonable,
                    'tileSize'       : self.tileSize,
                    'offGridTilemap' : offGridJsonable
                },
                savefile
            )
 

    def load(self, path):
        with open(path, 'r') as loadfile:
            levelData = json.load(loadfile)
        
        for k, v in levelData['onGridTilemap'].items():
            self.onGridTilemap[k] = Tile.fromDict(v)
        self.tileSize = levelData['tileSize']
        self.offGridTilemap = list(map(lambda it: Tile.fromDict(it), levelData['offGridTilemap']))

    def mockTiles(self):
        for idx in range(-10, 35):
            self.onGridTilemap[f'{idx}:10'] = Tile(clazz="crates", type=1, pos=(idx, 10))
            self.onGridTilemap[f'{idx}:20'] = Tile(clazz="crates", type=1, pos=(idx, 20))
            self.onGridTilemap[f'4:{1 + idx}'] = Tile(clazz="crates", type=2, pos=(4, 1+idx))


    def render(self, surface : pygame.Surface, offset = [0, 0]):
        for tile in self.offGridTilemap:
            surface.blit(self.game.assets[tile.clazz][tile.type], (tile.pos[0] - offset[0], tile.pos[1] - offset[1]))

        for x in range(offset[0] // self.tileSize, (offset[0] + surface.get_width()) // self.tileSize + 1):
            for y in range(offset[1] // self.tileSize, (offset[1] + surface.get_height()) // self.tileSize + 1):
                location = f'{x}:{y}'
                if location in self.onGridTilemap:
                    tile = self.onGridTilemap[location]
                    surface.blit(self.game.assets[tile.clazz][tile.type], (tile.pos[0] * self.tileSize - offset[0], tile.pos[1] * self.tileSize - offset[1]))


        # for _, tile in self.onGridTilemap.items():
        #     surface.blit(self.game.assets[tile.clazz][tile.type], (tile.pos[0] * self.tileSize - offset[0], tile.pos[1] * self.tileSize - offset[1]))
