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
A module for representing a World with an array representing each layer.

Classes:
---------
World:
    Represents a world in which organisms and food are distributed across a canvas.
"""

import random
import numpy as np
from typing import Union
import organism as org
from utilities import clamp


class World:
    """
    Represents a world in which organisms and food are distributed across a canvas.

    Attributes:
    -----------
    canvas_size (tuple): A tuple of two integers representing the dimensions of the canvas.

    food_distribution (numpy.ndarray): A numpy array of random integers between 0 and 160 of size `canvas_size`.

    temp_distribution (numpy.ndarray): A numpy array of random integers between 0 and 15 of size `canvas_size`.

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
            0, 160, self.canvas_size
        )
        self.temp_distribution: np.ndarray = np.random.random_integers(
            0, 16, self.canvas_size
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
        Update the state of the canvas

        Note:
        -----
        Updates the state of the world by iterating over each organism and updating its position based on its neural
        network's output. If another organism is not present at its current position after updating, it is removed from
        the current position and added to the new position. It also considers the direction of food around it.
        """
        for i in range(self.canvas_size[0]):
            for j in range(self.canvas_size[1]):
                organism = self.organism_distribution[i][j]
                neighbour_cells: np.ndarray = get_neighbour_cells(
                    (i, j), self.food_distribution
                )
                food_direction: int = (
                    int(np.argmax(neighbour_cells.flatten()))
                    if np.size(neighbour_cells.flatten())
                    else -1
                )

                # check if there is an organism at the current location
                if isinstance(organism, org.Organism):
                    # if enough food is available and if the temperature
                    # is ideal
                    if self.food_distribution[i][j] >= organism.characters[
                        2
                    ] and self.temp_distribution[i][j] in range(
                        organism.characters[0] - 4,
                        organism.characters[0] + 4,
                    ):
                        self.food_distribution[i][j] -= organism.characters[2]

                        neural_ouput: np.ndarray = (
                            organism.neural_network.run_neural_network(
                                np.array((food_direction, i, j))
                            )
                        )
                        new_coordinates = tuple(
                            clamp(
                                int(neural_ouput[k]) + (i, j)[k],
                                self.canvas_size[k] - 1,
                                0,
                            )
                            for k in range(2)
                        )

                        # While an organism already lives there the new coordinates change
                        while isinstance(
                            self.organism_distribution[new_coordinates[0]][
                                new_coordinates[1]
                            ],
                            org.Organism,
                        ):
                            new_coordinates = tuple(
                                clamp(
                                    new_coordinates[k]
                                    + random.choice((-1, 1)),
                                    self.canvas_size[k] - 1,
                                    0,
                                )
                                for k in range(2)
                            )

                        # move the organism
                        self.organism_distribution[i][j] = None
                        self.organism_distribution[new_coordinates[0]][
                            new_coordinates[1]
                        ] = organism

                    # if food is not available kill it and derive some food from its
                    # dead body.
                    else:
                        self.food_distribution[i][j] += organism.characters[2]
                        self.organism_distribution[i][j] = None


def get_neighbour_cells(
    coordinates: tuple[int, int], distribuion: np.ndarray
) -> np.ndarray:
    """Return the values of neighbouring cells around a given coordinate in a distribution.

    Args:
    -----
    coordinates (tuple[int, int]): The (x, y) coordinate for which to retrieve neighbouring cells.
    distribuion (np.ndarray): A 2D array of values representing a distribution of some kind.

    Returns:
    --------
    np.ndarray: A 2D array containing the values of neighbouring
    cells around the given coordinates. Specifically, this array
    contains a 3x3 subset of `distribution` centered around the
    given coordinates.
    """
    return distribuion[
        coordinates[0] - 1 : coordinates[0] + 1 + 1,
        coordinates[1] - 1 : coordinates[1] + 1 + 1,
    ]
