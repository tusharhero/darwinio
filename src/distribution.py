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

"""
A module for representing a 2D canvas with tiles containing organisms and food amounts.
"""

import random
import numpy as np
from typing import Union
from organism import Organism
import organism


class Tile:
    """
    A class representing a tile on the canvas.

    Attributes:
    -----------------------------------------------------------------------------------
        organism: An instance of the Organism class, or False if the tile is empty.
        food_amount: An integer representing the amount of food on the tile.
    """

    def __init__(self, organism: Union[Organism, str], food_amount: int):
        """
        Initializes an instance of the Tile class.
        """
        if isinstance(organism, Organism):
            self.organism = organism
        elif isinstance(organism, Organism):
            self.organism = False

        self.food_amount: int = food_amount


def get_random_tile() -> Tile:
    food_amount: int = random.randrange(16)
    random_organism: Organism = organism.get_random_organism()
    tile: Tile = Tile(random_organism, food_amount)
    return tile


class Canvas:
    """
    A class representing a 2D canvas with tiles containing organisms and food amounts.

    Attributes:
    -----------------------------------------------------------------------------------
        canvas_size: A tuple representing the dimensions of the canvas.
        canvas: A NumPy array representing the distribution of tiles on the canvas.
    """

    def __init__(self, canvas_size: tuple):
        """
        Initializes an instance of the Canvas class.
        """
        self.canvas_size: tuple = canvas_size
        self.canvas: np.ndarray = self.get_random_distribution()

    def get_random_distribution(self) -> np.ndarray:
        """
        Returns a NumPy array representing the random distribution of tiles on the canvas.
        """
        canvas = np.empty(self.canvas_size, dtype=object)

        for row in range(self.canvas_size[0]):
            for column in range(self.canvas_size[1]):
                canvas[row][column] = get_random_tile()
        return canvas
