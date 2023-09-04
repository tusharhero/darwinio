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

"""A module for representing a World with an array representing each
layer.

Classes:
---------
World: Represents a world in which organisms and food are distributed
across a canvas.

Functions:
----------
get_neighbour_cells: the values of neighbouring cells around a given
coordinate in a distribution.

get_distribution_population: Get the number of "truthy" values in the
distribution.

get_feasible_position: Finds a feasible position given a current
position, preferred position, and a distribution.

get_points_between_2_points: Return an array of coordinates of points
that lie on the line between two given points.
"""

from __future__ import annotations

import random
from typing import Union, cast

import numpy as np

import darwinio.organism as org


class Distribution:
    def __init__(self, data: np.ndarray) -> None:
        self.data: np.ndarray = data

    def get_population(self) -> int:
        """Get the number of "truthy" values in the distribution.

        Args:
        -----
        distribuion: A 2D array of values representing a distribution of some kind.
        """
        return np.count_nonzero(self.data)

    def get_neighbour_cells(self, coordinates: tuple[int, int]) -> np.ndarray:
        """Return the values of neighbouring cells around a given coordinate in a
        distribution.

        Args:
        -----
        coordinates: The (x, y) coordinate for which to retrieve neighbouring
        cells.

        Returns:
        --------
        np.ndarray: A 2D array containing the values of neighbouring cells around
        the given coordinates. Specifically, this array contains a 3x3 subset (not
        always) of ` distribution` centered around the given coordinates.
        """
        x, y = coordinates
        rows, cols = np.shape(self.data)
        return self.data[
            np.clip(x - 1, 0, rows) : np.clip(x + 1, 0, rows) + 1,
            np.clip(y - 1, 0, cols) : np.clip(y + 1, 0, cols) + 1,
        ]

    def get_feasible_position(
        self,
        current_position: tuple[int, int],
        preferred_position: tuple[int, int],
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
        x, y = self.data.shape
        possible_positions: np.ndarray = get_points_between_2_points(
            current_position, preferred_position
        )[:-1]

        for index, position in enumerate(possible_positions):
            row, column = tuple(position)
            if self.data[np.clip(column, 0, y - 1)][np.clip(row, 0, x - 1)]:
                return cast(
                    tuple[int, int],
                    tuple(
                        np.clip(
                            possible_positions[index - 1 if index != 0 else index][p],
                            0,
                            (y, x)[p] - 1,
                        )
                        for p in range(2)
                    ),
                )
        return cast(
            tuple[int, int],
            tuple(
                np.array(
                    [np.clip(preferred_position[p], 0, (x, y)[p] - 1) for p in range(2)]
                ).astype(int)
            ),
        )

    @classmethod
    def generate(
        cls,
        size: tuple[int, int],
        loc: int,
        scale: int,
    ) -> Distribution:
        """
        Generate a 2D numpy array of random values sampled from a
        normal distribution.

        Args:
        -----
        loc: An integer representing the mean of the normal
        distribution.

        scale: An integer representing the standard deviation of the
        normal distribution.

        size: A tuple of two integers representing the dimensions of
        the distribution.

        Returns:
        --------
        A 2D numpy array with the shape canvas_size where each element
        is a random value sampled from a normal distribution with the
        specified mean and standard deviation.
        """
        return cls(np.random.normal(loc=loc, scale=scale, size=size).astype(int))


class OrganismDistribution(Distribution):
    def get_reproduction_ratio(self) -> float:
        """
        Returns:
        --------
        The 'reproduction ratio', which is basically the
        number of asexuals per sexuals.
        """
        asexuals: int = 0
        sexuals: int = 0
        for row in self.data:
            for organism in row:
                if organism is not None:
                    if organism.genome_array[2] == 0:
                        asexuals += 1
                    else:
                        sexuals += 1
        return asexuals / sexuals if sexuals != 0 else np.NaN

    @classmethod
    def generate(
        cls,
        size: tuple[int, int],
        weights: tuple[float, float] = (0.1, 0.9),
        temp_range: tuple[int, int] = (30, 150),
        energy_range: tuple[int, int] = (100, 1000),
        reproductive_types: tuple[int, int] = (0, 1 + 1),
    ) -> OrganismDistribution:
        """
        Generate a random organism distribution.
        """
        return cls(
            np.array(
                [
                    [
                        random.choices(
                            (
                                org.Organism.random(
                                    temp_range,
                                    energy_range,
                                    reproductive_types,
                                ),
                                None,
                            ),
                            weights=weights,
                            k=1,
                        )[0]
                        for _ in range(size[1])
                    ]
                    for _ in range(size[0])
                ],
                dtype=object,
            )
        )


class World:
    """Represents a world in which organisms and food are distributed
    across a canvas.

    Attributes:
    -----------
    canvas_size: A tuple of two integers representing the dimensions
    of the canvas.

    mutation_factor: A value between 0 and 1 (inclusive) representing
    the probability of a mutation occurring in the offspring's genome.

    food_distribution: A numpy array of random integers between 0 and
    5000 of size `canvas_size`.

    organism_distribution: A 2D list of organisms and `None` values of
    size `canvas_size`.
    """

    def __init__(
        self,
        canvas_size: tuple[int, int],
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

        self.canvas_size: tuple[int, int] = canvas_size
        self.mutation_factor: float = mutation_factor

        self.food_distribution: Distribution = Distribution.generate(
            self.canvas_size,
            initial_food_avg,
            100,
        )

        self.temp_distribution: Distribution = Distribution.generate(
            self.canvas_size, initial_temp_avg, 50
        )
        self.organism_distribution: OrganismDistribution = (
            OrganismDistribution.generate(self.canvas_size)
        )

    def update_state(self) -> None:
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
                organism: org.Organism = self.organism_distribution.data[i][j]

                # check if there is an organism at the current location
                if organism is not None:
                    temp_range = get_integer_neighbors(organism.genome_array[0], 150)
                    food_value: int = self.food_distribution.data[i][j]

                    # name the conditions
                    has_enough_food: bool = food_value >= organism.genome_array[1]
                    is_in_ideal_temp: bool = (
                        self.temp_distribution.data[i][j] in temp_range
                    )
                    has_enough_food_for_reprod: bool = (
                        food_value >= 2 * organism.genome_array[1]
                    )
                    is_in_ideal_temp_for_reprod: bool = (
                        self.temp_distribution.data[i][j] in temp_range
                    )

                    if has_enough_food and is_in_ideal_temp:
                        self.food_distribution.data[i][j] -= organism.genome_array[1]
                        self.move(organism, (i, j))

                    if has_enough_food_for_reprod and is_in_ideal_temp_for_reprod:
                        self.reproduce(organism, (i, j))

                    # if food is not available kill it and derive some food
                    # from its dead body.
                    else:
                        self.food_distribution.data[i][j] += (
                            organism.genome_array[1] // 10
                        )
                        self.organism_distribution.data[i][j] = None

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
        neighbour_cells_food_dist: np.ndarray = (
            self.food_distribution.get_neighbour_cells((i, j))
        )
        neighbour_cells_temp_dist: np.ndarray = (
            self.temp_distribution.get_neighbour_cells((i, j))
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

        new_x, new_y = (
            organism.neural_network.run_neural_network(
                np.array((food_direction, temp_direction))
            )
        ).astype(int)

        new_coordinates: tuple = self.organism_distribution.get_feasible_position(
            (i, j),
            (i + new_x, j + new_y),
        )

        # move the organism
        self.organism_distribution.data[i][j] = None
        self.organism_distribution.data[new_coordinates[0]][
            new_coordinates[1]
        ] = organism

    def reproduce(self, organism: org.Organism, current_position: tuple[int, int]):
        """Reproduce the organism at the current position.

        Args:
        ------
        organism: An instance of the Organism class representing the organism
        to be reproduced.

        current_position: A tuple of two integers representing the current
        position of the organism.
        """
        i, j = current_position
        prefered_position: tuple[int, int] = cast(
            tuple[int, int],
            tuple((i, j)[p] + np.random.choice((-1, 1)) for p in range(2)),
        )
        x, y = self.organism_distribution.get_feasible_position(
            (i, j),
            prefered_position,
        )

        offspring: Union[org.Organism, None]

        # asexual
        if organism.genome_array[2] == 0:
            offspring = org.reproduce(organism, organism, 0.3)
        # sexual
        else:
            partner: Union[org.Organism, None] = None
            neighbour_cells: np.ndarray = (
                self.organism_distribution.get_neighbour_cells((i, j))
            )
            for row in neighbour_cells:
                for other_organism in row:
                    if other_organism:
                        partner = other_organism
                        break
            if partner is not None:
                offspring = org.reproduce(organism, partner, 0.3)
            else:
                offspring = None

            if offspring:
                self.organism_distribution.data[y][x] = offspring


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

    x_1, y_1 = np.array(point_1).astype(int)
    x_2, y_2 = np.array(point_2).astype(int)

    delta_y: int = y_2 - y_1
    delta_x: int = x_2 - x_1
    no_of_points: int = np.gcd(delta_y, delta_x) + 1

    x_coords: np.ndarray = np.linspace(x_1, x_2, no_of_points, dtype=int)
    y_coords: np.ndarray = np.linspace(y_1, y_2, no_of_points, dtype=int)

    # Combine the x and y coordinates into a single array
    points: np.ndarray = np.column_stack((x_coords, y_coords))

    return points


def get_integer_neighbors(value: int, radius: int) -> np.ndarray:
    """Get integers around a particular integer."""
    return np.arange(value - radius, value + radius + 1)
