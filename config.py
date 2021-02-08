WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
FPS = 60
TICK = 1

import pygame as pg
import color

class ScreenSurface:

    def __init__(self):
        self._screen = self.initialize()
        self._clock = pg.time.Clock()
        
    def initialize(self):
        return pg.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))

    def fillColor(self, color):
        self._screen.fill(color)

    def setClock(self):
        return self._clock.tick(FPS)

SCREEN = ScreenSurface()
SCREEN.fillColor(color.WHITE)
DT = SCREEN.setClock()
