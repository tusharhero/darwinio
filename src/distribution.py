# The GPLv3 License (GPLv3)

# Copyright (c) 2023 Tushar Maharana

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random
import numpy as np
from typing import Union
from organism import Organism
import organism


class Tile:
    def __init__(self, organism: Union[Organism, str], food_amount: int):
        if isinstance(organism, Organism):
            self.organism = organism
        elif isinstance(organism, Organism):
            self.organism = False

        self.food_amount: int = food_amount


class Canvas:
    def __init__(self, canvas_size: tuple):
        self.canvas_size: tuple = canvas_size
        self.canvas: np.ndarray = self.get_random_distribution()

    def get_random_distribution(self) -> np.ndarray:
        canvas = np.empty(self.canvas_size, dtype=object)
        for row in range(self.canvas_size[0]):
            for column in range(self.canvas_size[1]):
                food_amount: int = random.randrange(16)
                random_organism: Organism = organism.get_random_organism(
                    self.canvas_size
                )
                tile: Tile = Tile(random_organism, food_amount)
                canvas[row][column] = tile
        return canvas
