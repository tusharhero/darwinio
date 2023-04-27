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
Organism class and related stuff.

This module provides the Organism class, which represents an organism and its characteristics.
It also includes a function to generate a random organism.

Classes:
--------
Organism: A class representing an organism.

Functions:
--------
get_random_organism: A function to generate a random organism.

Note:
--------
Characteristics are stored as:
    0: ideal temperature
    1: trophic level
    2: energy requirement
    3: reproductive type
"""

import brain as brn
import genome as gn
import numpy as np
from typing import Union


class Organism:
    """
    A class representing an organism.

    Attributes:
    ---------
    genome: A string representing the organism's genome.

    characters: A NumPy array containing the organism's characteristics.

    neural_network: A neural network generated from the genome of the organism

    letters_per_character: The number of digits that would be used for representing
    each character.
    """

    def __init__(
        self,
        input_data: Union[str, np.ndarray],
        number_of_characters: int = 4,
        size_of_genome: int = 10,
        letters_per_character: int = 3,
    ) -> None:
        """
        Initializes an instance of the Organism class.

        Args:
        -----
        input_data : A string representing the organism's genome or a NumPy array
        containing the organism's characteristics.

        number_of_characters : The number of characteristics

        size_of_genome:  Its the length of the genome string.

        letters_per_character: The number of digits that would be used for representing
        each character.
        """

        self.letters_per_character: int = letters_per_character

        # check if input is genome or characteristics
        if isinstance(input_data, np.ndarray):
            self.genome: str = gn.encode_organism_characteristics(
                input_data,
                number_of_characters
                if number_of_characters > size_of_genome
                else size_of_genome,
                self.letters_per_character,
            )

            self.characters: np.ndarray = input_data

        elif isinstance(input_data, str):
            self.genome: str = input_data + gn.get_random_genome(
                size_of_genome - len(input_data)
            )

            self.characters: np.ndarray = gn.decode_organism_characteristics(
                input_data, number_of_characters, self.letters_per_character
            )
        # assign a neural_network generated from the the genome
        neural_structure = np.array([3, 2])
        weights: np.ndarray = brn.create_weights(self.genome, neural_structure)
        self.neural_network = brn.NeuralNetwork(weights, neural_structure)


def get_random_organism(
    size_of_genome: int = 8 * 3,
    letters_per_character: int = 3,
    allow_immortality: bool = False,
) -> Organism:
    """
    Generate a random organism.

    Args:
    -----
    size_of_genome : the size of the genome

    allow_immortality: allow the organism to be immortal

    Returns:
    ---------
    Organism: A random instance of the Organism class.
    """
    organism: Organism = Organism(
        input_data=gn.get_random_genome(size_of_genome),
        letters_per_character=letters_per_character,
    )
    if not allow_immortality:
        if organism.characters[2] == 0:
            organism.characters[2] = np.random.randint(1, 16)

    return organism


def reproduce(
    parent_1: Organism, parent_2: Organism, mutation_factor: float
) -> Organism:
    """
    Generate offspring of the two Organisms

    Args:
    -----
    parent_1 : One of the parent Organisms

    parent_2 : One of the parent Organisms

    mutation_factor: A value between 0 and 1 (inclusive) representing the probability
    of a mutation occurring in the offspring's genome.

    Returns:
    ---------
    offspring: Child of the parents.
    """
    offspring_genome: str = gn.generate_offspring_genome(
        parent_1.genome, parent_2.genome, mutation_factor
    )
    return Organism(offspring_genome)
