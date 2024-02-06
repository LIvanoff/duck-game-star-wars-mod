import pygame

from tilemap import *

class Entity:
    flip = False

    def __init__(self, game, type : str, pos : tuple, size : tuple) -> None:
        self.game = game
        self.type = type
        self.pos  = list(pos)
        self.size = size
        self.vel = [0, 0]
        self.pMov = [False, False]
        self.collisions = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
        self.currentAction = ''
        self.animationOffset = (0, 0)
        self.lastMov = [0, 0]
        self.setAction('idle')


    def collisionRect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    

    def setAction(self, action : str):
        if action != self.currentAction:
            self.currentAction = action
            self.animation = self.game.animations[f'{self.type}/{action}'].copy()
    

    def updateOld(self, tilemap : Tilemap, mov=(0, 0)):
        '''
        Старая функция апдейта, работает только с коллизиями
        '''
        self.collisions = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
        
        frameMov = (mov[0] + self.vel[0], mov[1] + self.vel[1])

        self.pos[0] += frameMov[0]
        entityRect = self.collisionRect()
        for rect in tilemap.collisionRects(self):
            if entityRect.colliderect(rect):
                if frameMov[0] > 0:
                    entityRect.right = rect.left
                    self.collisions['right'] = True
                if frameMov[0] < 0:
                    entityRect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entityRect.x

        self.pos[1] += frameMov[1]
        entityRect = self.collisionRect()
        for rect in tilemap.collisionRects(self):
            if entityRect.colliderect(rect):
                if frameMov[1] > 0:
                    entityRect.bottom = rect.top
                    self.collisions['down'] = True
                if frameMov[1] < 0:
                    entityRect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entityRect.y

        self.vel[1] = min(5, self.vel[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.vel[1] = 0

        self.animation.update()

    
    def update(self, tilemap : Tilemap, mov=(0, 0)):
        '''
        Функция апдейта работающая с тайлами а не боксами коллизий
        '''

        self.collisions = {'up' : False, 'down' : False, 'left' : False, 'right' : False}
        
        frameMov = (mov[0] + self.vel[0], mov[1] + self.vel[1])

        self.pos[0] += frameMov[0]
        entityRect = self.collisionRect()
        for tile in tilemap.collisionTiles(self):
            if entityRect.colliderect(tile.collisionRect):
                if frameMov[0] > 0:
                    if tile.clazz not in Tile.platforms():
                        entityRect.right = tile.collisionRect.left
                        self.collisions['right'] = True
                if frameMov[0] < 0:
                    if tile.clazz not in Tile.platforms():
                        entityRect.left = tile.collisionRect.right
                        self.collisions['left'] = True
                self.pos[0] = entityRect.x

        self.pos[1] += frameMov[1]
        entityRect = self.collisionRect()
        for tile in tilemap.collisionTiles(self):
            if entityRect.colliderect(tile.collisionRect):
                if frameMov[1] > 0:
                    if tile.clazz not in Tile.platforms():
                        entityRect.bottom = tile.collisionRect.top
                        self.collisions['down'] = True
                    else:
                        if tile.collisionRect.collidepoint(entityRect.midbottom):
                            entityRect.bottom = tile.collisionRect.top
                            self.collisions['down'] = True
                if frameMov[1] < 0:
                    if tile.clazz not in Tile.platforms():
                        entityRect.top = tile.collisionRect.bottom
                        self.collisions['up'] = True
                self.pos[1] = entityRect.y

        self.lastMov = mov

        self.vel[1] = min(5, self.vel[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.vel[1] = 0

        self.animation.update()

    
    def isMovingRight(self):
        self.flip = False
        self.pMov[1] = True

    def notMovingRight(self):
        self.pMov[1] = False

    def isMovingLeft(self):
        self.flip = True
        self.pMov[0] = True

    def notMovingLeft(self):
        self.pMov[0] = False

    
    def render(self, surface : pygame.Surface, offset = [0, 0]):
        # surface.blit(self.game.assets['player'], self.pos)
        surface.blit(
            pygame.transform.flip(self.animation.img(), self.flip, False), 
            (self.pos[0] - offset[0] + self.animationOffset[0], self.pos[1] - offset[1] + self.animationOffset[1])
        )