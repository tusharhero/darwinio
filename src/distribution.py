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
A module for representing the food and organism in the World
Classes:
---------
World:
    Represents a world in which organisms and food are distributed across a canvas.
"""

import random
import numpy as np
from typing import Union
import organism as org


class World:
    """
    Represents a world in which organisms and food are distributed across a canvas.

        Attributes:
        -----------
            canvas_size (tuple): A tuple of two integers representing the dimensions of the canvas.

            food_distribution (numpy.ndarray): A numpy array of random integers between 0 and 15 of size `canvas_size`.

            organism_distribution (list[list[Union[org.Organism, None]]]): A 2D list of organisms and `None` values
                of size `canvas_size`.
    """

    def __init__(self, canvas_size: tuple):
        """
        Initializes a new World instance.

        Args:
        -----
            canvas_size (tuple): A tuple of two integers representing the dimensions of the canvas.

        """
        self.canvas_size: tuple = canvas_size
        self.food_distribution: np.ndarray = np.random.random_integers(
            0, 15, self.canvas_size
        )
        self.organism_distribution: list[list[Union[org.Organism, None]]] = [
            [
                random.choice((org.get_random_organism(), None))
                for _ in range(self.canvas_size[1])
            ]
            for _ in range(self.canvas_size[0])
        ]

    def update_state(self):
        """
        Update the state of the canvas.

        Note:
        -----
            Updates the state of the world by iterating over each organism and updating its position based on its neural
            network's output. If the organism is not present at its current position after updating, it is removed from
            the current position and added to the new position.
        """

        for i in range(self.canvas_size[0]):
            for j in range(self.canvas_size[1]):
                organism = self.organism_distribution[i][j]

                if isinstance(organism, org.Organism):
                    x, y = organism.neural_network.run_neural_network(
                        np.array((i, j))
                    )
                    self.organism_distribution[i][j] = None
                    self.organism_distribution[x][y] = organism
