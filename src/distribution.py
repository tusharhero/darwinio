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
World: Represents a world in which organisms and food are distributed across
a canvas.

Functions:
----------
get_neighbour_cells: the values of neighbouring cells around a given
coordinate in a distribution.
"""

import random
from typing import Union
import numpy as np
import organism as org
import utilities as utils


class World:
    """
    Represents a world in which organisms and food are distributed across a
    canvas.

    Attributes:
    -----------
    canvas_size (tuple): A tuple of two integers representing the dimensions
    of the canvas.

    food_distribution (numpy.ndarray): A numpy array of random integers between
    0 and 500000 of size `canvas_size`.

    organism_distribution (list[list[Union[org.Organism, None]]]): A 2D list
    of organisms and `None` values of size `canvas_size`.
    """

    def __init__(self, canvas_size: tuple, mutation_factor: float = 0.3):
        """
        Initializes a new World instance.

        Args:
        -----
        canvas_size (tuple): A tuple of two integers representing the
        dimensions of the canvas.

        mutation_factor: A value between 0 and 1 (inclusive) representing the
        probability of a mutation occurring in the offspring's genome.
        """

        self.canvas_size: tuple = canvas_size
        self.mutation_factor: float = mutation_factor
        self.food_distribution: np.ndarray = np.random.random_integers(
            0, 500000, self.canvas_size
        )

        # Randomly distribute the organisms
        self.organism_distribution = np.array(
            [
                [
                    random.choice((org.get_random_organism(), None))
                    for _ in range(self.canvas_size[1])
                ]
                for _ in range(self.canvas_size[0])
            ],
            dtype=object,
        )

    def update_state(self):
        """
        Update the state of the canvas.

        Note:
        -----
        Updates the state of the world by iterating over each organism and
        updating its position based on its neural network's output. If
        another organism is not present at its current position after updating,
        it is removed from the current position and added to the new
        position. It also considers the direction of food around it.
        """

        rows, cols = self.canvas_size

        for i in range(rows):
            for j in range(cols):
                organism = self.organism_distribution[i][j]

                neighbour_cells_food_dist: np.ndarray = get_neighbour_cells(
                    (i, j), self.food_distribution
                )

                food_direction = int(
                    np.argmax(neighbour_cells_food_dist)
                    if np.size(neighbour_cells_food_dist.flatten())
                    else -1
                )

                # check if there is an organism at the current location
                if isinstance(organism, org.Organism):
                    # if enough food is available
                    if self.food_distribution[i][j] >= organism.characters[2]:
                        self.food_distribution[i][j] -= organism.characters[2]

                        nx, ny = organism.neural_network.run_neural_network(
                            np.array((food_direction, i, j))
                        )

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

                    elif (
                        self.food_distribution[i][j]
                        >= 2 * organism.characters[2]
                    ):
                        prefered_position = tuple(
                            [
                                (i, j)[p] + random.choice((-1, 1))
                                for p in range(2)
                            ]
                        )
                        x, y = get_feasible_position(
                            (i, j),
                            prefered_position,
                            self.organism_distribution,
                        )
                        if organism.characters[3] == 0:
                            offspring: Union[
                                org.Organism, None
                            ] = org.reproduce(organism, organism, 0.3)
                        else:
                            partner: Union[org.Organism, None] = None
                            neighbour_cells: np.ndarray = get_neighbour_cells(
                                (i, j), self.organism_distribution
                            )
                            for row in neighbour_cells:
                                for organism in row:
                                    if organism:
                                        partner: Union[
                                            org.Organism, None
                                        ] = organism
                                        break
                            if isinstance(partner, org.Organism):
                                offspring: Union[
                                    org.Organism, None
                                ] = org.reproduce(organism, partner, 0.3)
                            else:
                                offspring: Union[org.Organism, None] = None

                            if offspring:
                                self.organism_distribution[y][x] = offspring

                    # if food is not available kill it and derive some food
                    # from its dead body.
                    else:
                        self.food_distribution[i][j] += (
                            organism.characters[2] * 10
                        )
                        self.organism_distribution[i][j] = None

    def get_next_gen(self):
        """
        Calculate the distribution of organisms for the next generation based
        on the current distribution.

        Note:
        ----
        This method applies the rules of the simulation to the current
        distribution of organisms and produces the distribution for the next
        generation. The current distribution is first converted to a numpy
        array for processing. Then, for each cell in the grid, the function
        checks whether the organism at that cell can reproduce. If the
        organism is asexual, it creates an offspring and adds food to the
        current cell. If the organism is sexual, the function searches for a
        valid partner among its neighboring cells. If a partner is found, the
        two organisms reproduce to produce an offspring. The distribution of
        organisms for the next generation is stored in a list of lists, and
        is updated at the end of the function.
        """

        # Convert current generation to a binary numpy array for processing
        reproductive_distribution = np.array(
            [
                [
                    1 if isinstance(organism, org.Organism) else 0
                    for organism in column
                ]
                for column in self.organism_distribution
            ]
        )

        next_gen_organism_distribution = np.array(
            [
                [None for _ in range(self.canvas_size[1])]
                for _ in range(self.canvas_size[0])
            ]
        )

        for i in range(self.canvas_size[0]):
            for j in range(self.canvas_size[1]):
                organism = self.organism_distribution[i][j]

                if isinstance(organism, org.Organism):
                    # If the organism is asexual, create offspring
                    if organism.characters[3] == 0:
                        next_gen_organism_distribution[i][j] = org.reproduce(
                            organism, organism, self.mutation_factor
                        )
                        self.food_distribution[i][j] += (
                            organism.characters[2] * 10
                        )
                        reproductive_distribution[i][j] = 0
                    # If organism is sexual
                    else:
                        neighbours: np.ndarray = get_neighbour_cells(
                            (i, j), reproductive_distribution
                        )
                        x = y = 0

                        # try to find a valid partner
                        partner = self.organism_distribution[i + x - 1][
                            j + y - 1
                        ]
                        while (
                            neighbours[x][y] != 0
                            and partner.characters[3] == 0
                            if isinstance(partner, org.Organism)
                            else True
                        ):
                            x += 1
                            y += 1
                            partner = self.organism_distribution[i + x - 1][
                                j + y - 1
                            ]
                            # If all neighbours have been checked, break out
                            # of loop
                            if x == len(neighbours) and y == len(
                                neighbours[0]
                            ):
                                partner = None
                                break

                        # if partner has been found reproduce
                        if isinstance(partner, org.Organism):
                            next_gen_organism_distribution[i][
                                j
                            ] = org.reproduce(
                                organism, partner, self.mutation_factor
                            )
                            # Make sure the partner doesn't reproduce with
                            # someother organism
                            reproductive_distribution[i][j] = 0
                            reproductive_distribution[i + x - 1][j + y - 1] = 0

        self.organism_distribution: np.ndarray = next_gen_organism_distribution


def get_neighbour_cells(
    coordinates: tuple[int, int], distribuion: np.ndarray
) -> np.ndarray:
    """
    Return the values of neighbouring cells around a given coordinate in a
    distribution.

    Args:
    -----
    coordinates (tuple[int, int]): The (x, y) coordinate for which to
    retrieve neighbouring cells.

    distribuion (np.ndarray): A 2D array of values representing a
    distribution of some kind.

    Returns:
    --------
    np.ndarray: A 2D array containing the values of neighbouring cells around
    the given coordinates. Specifically, this array contains a 3x3 subset(not
    always) of ` distribution` centered around the given coordinates.
    """
    x, y = coordinates
    rows, cols = np.shape(distribuion)
    return distribuion[
        utils.clamp(x - 1, rows, 0) : utils.clamp(x + 1, rows, 0) + 1,
        utils.clamp(y - 1, cols, 0) : utils.clamp(y + 1, cols, 0) + 1,
    ]


def get_distribution_population(distribution: np.ndarray) -> int:
    """
    get the number of "truthy" values in the distribution

    Args:
    -----
    distribuion (np.ndarray): A 2D array of values representing a
    distribution of some kind.
    """
    return sum(
        [sum([1 if cell else 0 for cell in row]) for row in distribution]
    )


def get_feasible_position(
    current_position: tuple[int, int],
    preferred_position: tuple[int, int],
    distribution: np.ndarray,
) -> tuple[int, int]:
    """
    Finds a feasible position given a current position, preferred position, and
    a distribution.

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
    A tuple containing the x and y coordinates of a feasible position. If
    there are no feasible positions between the current and preferred positions,
    returns the preferred position if it is feasible, otherwise returns the
    current position.
    """
    possible_positions: np.ndarray = get_points_between_2_points(
        current_position, preferred_position
    )

    for index, position in enumerate(possible_positions):
        row, column = tuple(position)
        if distribution[column][row]:
            return tuple(
                possible_positions[index - 1 if index != 0 else index]
            )
    return tuple(np.array(preferred_position).astype(int))


def get_points_between_2_points(
    point_1: tuple[int, int], point_2: tuple[int, int]
) -> np.ndarray:
    """
    Return an array of coordinates of points that lie on the line between two
    given points.

    Args:
    -----
    point_1 (tuple): A tuple of two integers that represent the (x, y)
    coordinates of the first point.

    point_2 (tuple): A tuple of two integers that represent the (x, y)
    coordinates of the second point.

    Returns:
    -----
    np.ndarray: An array of coordinates of the points that lie on the line
    between the two given points.

    Note:
    -----
    The function calculates the coordinates of the points that lie on the
    line between the two input points, and returns an array of these
    coordinates. The function first determines the slope and intercept of the
    line connecting the two input points. If the line is vertical, the
    function returns an array of points with the same x coordinate and a
    range of y coordinates. Otherwise, the function calculates the
    coordinates of the points on the line using the slope and intercept, and
    returns an array of these coordinates. The returned array is sorted by
    distance from the first input point.
    """

    x1, y1 = np.array(point_1).astype(int)
    x2, y2 = np.array(point_2).astype(int)

    # Calculate the slope of the line
    if x1 == x2:
        # Handle the special case where the line is vertical
        x_coords: np.ndarray = np.full(abs(y2 - y1) + 1, x1)
        y_coords: np.ndarray = np.arange(min(y1, y2), max(y1, y2) + 1)
    else:
        slope: float = (y2 - y1) / (x2 - x1)
        intercept: float = y1 - slope * x1

        # Calculate the coordinates of the points on the line
        x_coords: np.ndarray = np.arange(min(x1, x2), max(x1, x2) + 1)
        y_coords: np.ndarray = np.around(slope * x_coords + intercept).astype(
            int
        )

    # Combine the x and y coordinates into a single array
    points: np.ndarray = np.column_stack((x_coords, y_coords))

    # Remove duplicate points
    points: np.ndarray = np.unique(points, axis=0)

    # Sort the points by distance from the first input point
    distances: np.ndarray = np.linalg.norm(points - point_1, axis=1)
    sorted_indices: np.ndarray = np.argsort(distances)
    points: np.ndarray = points[sorted_indices]

    return points.astype(int)
