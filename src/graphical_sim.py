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


# CONSTANTS
X_SIZE, Y_SIZE = CANVAS_SIZE = (10, 10)
X_CELL_SIZE, Y_CELL_SIZE = CELL_SIZE = (20, 20)


# initialize
pg.init()
screen: pg.Surface = pg.display.set_mode((X_SIZE * 20, Y_SIZE * 20))
pg.display.set_caption("darwinio")
clock = pg.time.Clock()


class Button:
    def __init__(
        self,
        text: str,
        size: tuple[int, int],
        position: tuple[int, int],
        max_elevation: int = 6,
        font=pg.font.Font(None, 30),
    ) -> None:
        # core attributes
        self.max_elevation: int = max_elevation
        self.elevation: int = max_elevation
        self.position: tuple[int, int] = position

        # top rectangle
        self.top_rect = pg.Rect(position, size)
        self.top_color_not_pressed = "#475F77"
        self.top_color_pressed = "#D74B4B"
        self.top_color = self.top_color_not_pressed

        # bottom rectangle
        self.bottom_rect = pg.Rect(position, (size[0], max_elevation))
        self.bottom_color = "#35485E"

        # text
        self.font: pg.font.Font = font
        self.text_color = "#FFFFFF"
        self.text_surface = font.render(text, False, self.text_color)
        self.text_rect = self.text_surface.get_rect(
            center=self.top_rect.center
        )

    def draw(self):
        self.top_rect.x = self.position[0] - self.elevation
        self.top_rect.y = self.position[1] - self.elevation

        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.elevation
        self.bottom_rect.width = self.top_rect.width + self.elevation

        pg.draw.rect(screen, self.bottom_color, self.bottom_rect)
        pg.draw.rect(screen, self.top_color, self.top_rect)
        screen.blit(self.text_surface, self.text_rect)

    def check_click(self, events: list[pg.event.Event]) -> bool:
        mouse_pos: tuple[int, int] = pg.mouse.get_pos()
        pressed = False
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.top_color_pressed
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.elevation = 0
                    pressed = True
                else:
                    self.elevation = self.max_elevation
        else:
            self.top_color = self.top_color_not_pressed
        return pressed


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


organism_surface = pg.Surface((200, 200))
world = World(CANVAS_SIZE, organism_surface)
button = Button("click", (100, 40), (90, 100))

# Main game loop
i = 0
while True:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    screen.fill("white")
    world.render()
    button.draw()
    if button.check_click(events):
        print(1)
    pg.display.update()
    if i % 60 == 0:
        world.update_state()
    i += 1
    clock.tick(60)
