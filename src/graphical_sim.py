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
import distribution as dist
import numpy as np


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
                organism: np.ndarray = self.organism_distribution[i][j]
                if organism is not None:
                    screen.blit(
                        self.organism_surface,
                        (i * X_CELL_SIZE, j * Y_CELL_SIZE),
                    )


# CONSTANTS
X_SIZE, Y_SIZE = CANVAS_SIZE = (10, 10)
X_CELL_SIZE, Y_CELL_SIZE = CELL_SIZE = (20, 20)

# initialize
pg.init()
screen: pg.Surface = pg.display.set_mode((X_SIZE * 20, Y_SIZE * 20))
pg.display.set_caption("darwinio")
clock = pg.time.Clock()

organism_surface = pg.Surface((20, 20))
world = World(CANVAS_SIZE, organism_surface)

# Main game loop
i = 0
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    screen.fill("white")
    world.render()
    world.update_state()
    if i % 10 == 0:
        pg.display.update()
    i += 1
    clock.tick(60)
