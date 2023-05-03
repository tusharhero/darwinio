# The GPLv3 License (GPLv3)

# Copyright (c) 2023 Tushar Maharana, and Mihir Nallagonda

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame as pg
import sys
import time
import distribution as dist
import numpy as np


# CONSTANTS
X_SIZE, Y_SIZE = CANVAS_SIZE = (30, 30)
X_CELL_SIZE, Y_CELL_SIZE = CELL_SIZE = (20, 20)


# initialize
pg.init()
screen: pg.Surface = pg.display.set_mode((X_SIZE * 20, Y_SIZE * 20))
pg.display.set_caption("darwinio")
clock = pg.time.Clock()


class World(dist.World):
    def __init__(
        self,
        canvas_size: tuple,
        organism_surface: pg.Surface,
        mutation_factor: float = 0.3,
    ):
        super().__init__(canvas_size, mutation_factor)
        self.organism_surface = organism_surface

    def render(self):
        x, y = self.canvas_size
        for i in range(x):
            for j in range(y):
                organism = self.organism_distribution[i][j]
                if organism is not None:
                    organism_surface.fill(f"#{organism.genome[:6]}")
                    screen.blit(
                        self.organism_surface,
                        (i * X_CELL_SIZE, j * Y_CELL_SIZE),
                    )


organism_surface = pg.Surface(CELL_SIZE)
organism_surface.fill("white")
world = World(CANVAS_SIZE, organism_surface)

timer = 0
while True:
    dt = clock.tick(60) / 1000
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    screen.fill("black")
    timer += 1 / dt
    if timer >= 60:
        timer = 0
        start = time.time()
        world.update_state()
        print("upt", time.time() - start)
    world.render()
    pg.display.update()
