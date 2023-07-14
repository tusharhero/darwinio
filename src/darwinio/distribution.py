# The GPLv3 License (GPLv3)

# Copyright © 2023 Tushar Maharana, and Mihir Nallagonda

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

"""A module for representing a World with an array representing each layer.

Classes:
---------
World: Represents a world in which organisms and food are distributed across a
canvas.

Functions:
----------
get_neighbour_cells: the values of neighbouring cells around a given coordinate
in a distribution.

get_distribution_population: Get the number of "truthy" values in the
distribution.

get_feasible_position: Finds a feasible position given a current position,
preferred position, and a distribution.

get_points_between_2_points: Return an array of coordinates of points that lie
on the line between two given points.
"""

from __future__ import annotations
from typing import Union
import numpy as np
import random
import darwinio.organism as org


class World:
    """Represents a world in which organisms and food are distributed across a
    canvas.

    Attributes:
    -----------
    canvas_size: A tuple of two integers representing the dimensions of the
    canvas.

    mutation_factor: A value between 0 and 1 (inclusive) representing the
    probability of a mutation occurring in the offspring's genome.

    food_distribution: A numpy array of random integers between 0 and 5000 of
    size `canvas_size`.

    organism_distribution: A 2D list of organisms and `None` values of size
    `canvas_size`.
    """

    def __init__(
        self,
        canvas_size: tuple,
        mutation_factor: float = 0.3,
        initial_food_avg: int = 500,
        initial_temp_avg: int = 315,
    ):
        """Initializes a new World instance.

        Args:
        ------
        canvas_size: A tuple of two integers representing the dimensions of the
        canvas.

        mutation_factor: A value between 0 and 1 (inclusive) representing the
        probability of a mutation occurring in the offspring's genome.

        initial_food_distribution: The range of values which will be found in
        the food variation.

        initial_temp_distribution: The range of values which will be found in
        the temp variation.
        """

        self.canvas_size: tuple = canvas_size
        self.mutation_factor: float = mutation_factor

        self.food_distribution: np.ndarray = self.generate_distribution(
            initial_food_avg, 100
        )

        self.temp_distribution: np.ndarray = self.generate_distribution(
            initial_temp_avg, 50
        )
        self.organism_distribution: np.ndarray = (
            self.generate_organism_distribution()
        )

    def update_state(self):
        """Update the state of the canvas.

        Note:
        -----
        Updates the state of the world by iterating over each organism and
        updating its position based on its neural network's output. If another
        organism is not present at its current position after updating, it is
        removed from the current position and added to the new position. It
        also considers the direction of food around it. Then it allows the
        organism to reproduce if it has access to 2x the amount of food.
        """

        rows, cols = self.canvas_size

        for i in range(rows):
            for j in range(cols):
                organism = self.organism_distribution[i][j]

                # check if there is an organism at the current location
                if organism is not None:
                    temp_range = np.arange(0, organism.genome_array[0])
                    food_value = self.food_distribution[i][j]

                    # name the conditions

                    has_enough_food: bool = (
                        food_value >= organism.genome_array[2]
                    )
                    is_in_ideal_temp: bool = (
                        self.temp_distribution[i][j] in temp_range
                    )
                    has_enough_food_for_reprod: bool = (
                        food_value >= 2 * organism.genome_array[2]
                    )
                    is_in_ideal_temp_for_reprod: bool = (
                        self.temp_distribution[i][j] in temp_range
                    )

                    if has_enough_food and is_in_ideal_temp:
                        self.food_distribution[i][j] -= organism.genome_array[
                            2
                        ]
                        self.move(organism, (i, j))

                    if (
                        has_enough_food_for_reprod
                        and is_in_ideal_temp_for_reprod
                    ):
                        self.reproduce(organism, (i, j))

                    # if food is not available kill it and derive some food
                    # from its dead body.
                    else:
                        self.food_distribution[i][j] += (
                            organism.genome_array[2] * 10
                        )
                        self.organism_distribution[i][j] = None

    def move(self, organism: org.Organism, current_position: tuple[int, int]):
        """Move the organism to a new position based on the current position
        and environmental conditions.

        Args:
        ------
        organism: An instance of the Organism class representing the organism
        to be moved.

        current_position: A tuple of two integers representing the current
        position of the organism.
        """

        i, j = current_position
        neighbour_cells_food_dist: np.ndarray = get_neighbour_cells(
            (i, j), self.food_distribution
        )
        neighbour_cells_temp_dist: np.ndarray = get_neighbour_cells(
            (i, j), self.temp_distribution
        )

        food_direction = int(
            np.argmax(neighbour_cells_food_dist)
            if np.size(neighbour_cells_food_dist.flatten())
            else -1
        )
        temp_direction = int(
            np.argmax(neighbour_cells_temp_dist)
            if np.size(neighbour_cells_temp_dist.flatten())
            else -1
        )

        nx, ny = (
            organism.neural_network.run_neural_network(
                np.array((food_direction, temp_direction))
            )
        ).astype(int)

        new_coordinates: tuple = get_feasible_position(
            (i, j),
            (i + nx, j + ny),
            self.organism_distribution,
        )

        # move the organism
        self.organism_distribution[i][j] = None
        self.organism_distribution[new_coordinates[0]][
            new_coordinates[1]
        ] = organism

    def reproduce(
        self, organism: org.Organism, current_position: tuple[int, int]
    ):
        """Reproduce the organism at the current position.

        Args:
        ------
        organism: An instance of the Organism class representing the organism
        to be reproduced.

        current_position: A tuple of two integers representing the current
        position of the organism.
        """
        i, j = current_position
        prefered_position = tuple(
            [(i, j)[p] + np.random.choice((-1, 1)) for p in range(2)]
        )
        x, y = get_feasible_position(
            (i, j),
            prefered_position,
            self.organism_distribution,
        )

        # asexual
        if organism.genome_array[3] == 0:
            offspring: Union[org.Organism, None] = org.reproduce(
                organism, organism, 0.3
            )
        # sexual
        else:
            partner: Union[org.Organism, None] = None
            neighbour_cells: np.ndarray = get_neighbour_cells(
                (i, j), self.organism_distribution
            )
            for row in neighbour_cells:
                for other_organism in row:
                    if other_organism:
                        partner = other_organism
                        break
            if partner is not None:
                offspring: Union[org.Organism, None] = org.reproduce(
                    organism, partner, 0.3
                )
            else:
                offspring: Union[org.Organism, None] = None

            if offspring:
                self.organism_distribution[y][x] = offspring

    def generate_distribution(self, loc: int, scale: int) -> np.ndarray:
        """
        Generate a 2D numpy array of random values sampled from a normal
        distribution.

        Args:
        -----
        loc: An integer representing the mean of the normal distribution.

        scale: An integer representing the standard deviation of the normal
        distribution.

        Returns:
        --------
        A 2D numpy array with the shape canvas_size where each element is a
        random value sampled from a normal distribution with the specified mean
        and standard deviation.
        """
        return np.random.normal(
            loc=loc, scale=scale, size=self.canvas_size
        ).astype(int)

    def generate_organism_distribution(
        self,
        weights: tuple[float, float] = (0.1, 0.9),
        temp_range: tuple[int, int] = (230, 400),
        trophic_level_range: tuple[int, int] = (0, 3),
        energy_range: tuple[int, int] = (100, 1000),
        reproductive_types: tuple[int, int] = (0, 1 + 1),
    ) -> np.ndarray:
        return np.array(
            [
                [
                    random.choices(
                        (
                            org.get_random_organism(
                                temp_range,
                                trophic_level_range,
                                energy_range,
                                reproductive_types,
                            ),
                            None,
                        ),
                        weights=weights,
                        k=1,
                    )[0]
                    for _ in range(self.canvas_size[1])
                ]
                for _ in range(self.canvas_size[0])
            ],
            dtype=object,
        )

    def get_population(self) -> int:
        """Gets you the population of the world."""
        return get_distribution_population(self.organism_distribution)


def get_neighbour_cells(
    coordinates: tuple[int, int], distribuion: np.ndarray
) -> np.ndarray:
    """Return the values of neighbouring cells around a given coordinate in a
    distribution.

    Args:
    -----
    coordinates: The (x, y) coordinate for which to retrieve neighbouring
    cells.

    distribuion: A 2D array of values representing a distribution of some kind.

    Returns:
    --------
    np.ndarray: A 2D array containing the values of neighbouring cells around
    the given coordinates. Specifically, this array contains a 3x3 subset (not
    always) of ` distribution` centered around the given coordinates.
    """
    x, y = coordinates
    rows, cols = np.shape(distribuion)
    return distribuion[
        np.clip(x - 1, 0, rows) : np.clip(x + 1, 0, rows) + 1,
        np.clip(y - 1, 0, cols) : np.clip(y + 1, 0, cols) + 1,
    ]


def get_distribution_population(distribution: np.ndarray) -> int:
    """Get the number of "truthy" values in the distribution.

    Args:
    -----
    distribuion: A 2D array of values representing a distribution of some kind.
    """
    return np.count_nonzero(distribution)


def get_feasible_position(
    current_position: tuple[int, int],
    preferred_position: tuple[int, int],
    distribution: np.ndarray,
) -> tuple[int, int]:
    """Finds a feasible position given a current position, preferred
    position, and a distribution.

    Args:
    ----
    current_position: A tuple containing the x and y coordinates of the current
    position.

    preferred_position: A tuple containing the x and y coordinates of the
    preferred position.

    distribution: A 2D numpy array representing the distribution of feasible
    positions.

    Returns:
    -------
    A tuple containing the x and y coordinates of a feasible position. If there
    are no feasible positions between the current and preferred positions,
    returns the preferred position if it is feasible, otherwise returns the
    current position.
    """
    x, y = distribution.shape
    possible_positions: np.ndarray = get_points_between_2_points(
        current_position, preferred_position
    )[:-1]

    for index, position in enumerate(possible_positions):
        row, column = tuple(position)
        if distribution[np.clip(column, 0, y - 1)][np.clip(row, 0, x - 1)]:
            return tuple(
                [
                    np.clip(
                        possible_positions[index - 1 if index != 0 else index][
                            p
                        ],
                        0,
                        (y, x)[p] - 1,
                    )
                    for p in range(2)
                ]
            )
    return tuple(
        np.array(
            [
                np.clip(preferred_position[p], 0, (x, y)[p] - 1)
                for p in range(2)
            ]
        ).astype(int)
    )


def get_points_between_2_points(
    point_1: tuple[int, int], point_2: tuple[int, int]
) -> np.ndarray:
    """Return an array of coordinates of points that lie on the line between
    two given points.

    Args:
    -----
    point_1: A tuple of two integers that represent the (x, y) coordinates of
    the first point.

    point_2: A tuple of two integers that represent the (x, y) coordinates of
    the second point.

    Returns:
    -----
    np.ndarray: An array of coordinates of the points that lie on the line
    between the two given points.(inclusive of point1 and point2)

    Note:
    -----
    The function calculates the coordinates of the points that lie on the line
    between the two input points, and returns an array of these coordinates. We
    first get the number of possible points integer points. And then finds such
    points such that they are linearly placed. And then combines them.
    """

    x1, y1 = np.array(point_1).astype(int)
    x2, y2 = np.array(point_2).astype(int)

    Dy: int = y2 - y1
    Dx: int = x2 - x1
    no_of_points: int = np.gcd(Dy, Dx) + 1

    x_coords: np.ndarray = np.linspace(x1, x2, no_of_points, dtype=int)
    y_coords: np.ndarray = np.linspace(y1, y2, no_of_points, dtype=int)

    # Combine the x and y coordinates into a single array
    points: np.ndarray = np.column_stack((x_coords, y_coords))

    return points


def get_integer_neighbors(value: int, radius: int) -> np.ndarray:
    """Get integers around a particular integer."""
    return np.arange(value - radius, value + radius + 1)
