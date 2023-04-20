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

"""
A module for representing a 2D canvas with tiles containing organisms and food amounts.

This module contains two classes: Tile and Canvas.
Tile represents a tile on the canvas and contains an organism and food amount.
Canvas represents a 2D canvas of tiles and contains a NumPy array representing
the distribution of tiles on the canvas.

The module also contains a function for generating a random Tile object.

Classes:
---------
Tile:
    A class representing a tile on the canvas.

Canvas:
    A class representing a 2D canvas with tiles containing organisms and food amounts.

Functions:
----------
get_random_tile() -> Tile:
    Returns a randomly generated Tile object.
"""

import random
import numpy as np
from typing import Union
from organism import Organism
import organism


class Tile:
    """
    A class representing a tile on the canvas.
        organism: An instance of the Organism class, or None if the tile is empty.

        food_amount: An integer representing the amount of food on the tile.
    """

    def __init__(self, organism: Union[Organism, None], food_amount: int):
        """
        Initializes an instance of the Tile class.
        """
        if isinstance(organism, Organism):
            self.organism = organism
        else:
            self.organism = None

        self.food_amount: int = food_amount


def get_random_tile() -> Tile:
    """
    Returns a randomly generated Tile object.
    """
    food_amount: int = random.randrange(16)
    random_organism: Organism = organism.get_random_organism()
    tile: Tile = Tile(random.choice((random_organism, None)), food_amount)
    return tile


class World:
    """
    A class representing a world with canvas containing tiles containing
    organisms and food amounts.

    Attributes:
    -----------
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
