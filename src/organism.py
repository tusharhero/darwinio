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

"""Organism class and related stuff.

Classes:
--------
Organism: A class representing an organism.

Functions:
--------
get_random_organism: A function to generate a random organism.

reproduce: Generate offspring of the two Organisms.

Note:
--------
Characters are stored as:
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
    """A class representing an organism.

    Attributes:
    ---------
    genome: A string representing the organism's genome.

    characters: A NumPy array containing the organism's characters.

    neural_network: A neural network generated from the genome of the organism

    letters_per_character: The number of digits that would be used for
    representing each character.
    """

    def __init__(
        self,
        genome_array: np.ndarray,
    ) -> None:
        """Initializes an instance of the Organism class.

        Args:
        -----
        input_data : A string representing the organism's genome or a NumPy
        array containing the organism's characters.

        number_of_characters : The number of characters

        size_of_genome: It's the length of the genome string.

        letters_per_character: The number of digits that would be used for
        representing each character.
        """

        self.genome_array: np.ndarray = genome_array

        # assign a neural_network generated from the genome
        neural_structure = np.array([2, 2])
        weights: np.ndarray = brn.create_weights(
            self.genome_array, neural_structure
        )
        self.neural_network = brn.NeuralNetwork(weights, neural_structure)


def get_random_organism(
    temp_range,
    trophic_level_range,
    energy_range,
    reproductive_types,
) -> Organism:
    """Generate a random organism.

    Args:
    -----
    size_of_genome : the size of the genome

    letters_per_character: The number of digits that would be used for
    representing each character.

    Returns:
    ---------
    Organism: A random instance of the Organism class.
    """

    characters: np.ndarray = np.array(
        (
            np.random.randint(*temp_range, dtype=np.int64),
            np.random.randint(*trophic_level_range, dtype=np.int64),
            np.random.randint(*energy_range, dtype=np.int64),
            np.random.randint(*reproductive_types, dtype=np.int64),
        )
    )

    organism: Organism = Organism(characters)

    return organism


def reproduce(
    parent_1: Organism, parent_2: Organism, mutation_factor: float
) -> Organism:
    """Generate offspring of the two Organisms.

    Args:
    -----
    parent_1: One of the parent Organisms

    parent_2: One of the parent Organisms

    mutation_factor: A value between 0 and 1 (inclusive) representing the
    probability of a mutation occurring in the offspring's genome.

    Returns:
    ---------
    offspring: Child of the parents.
    """
    offspring_genome: np.ndarray = gn.generate_offspring_genome(
        parent_1.genome_array, parent_2.genome_array, mutation_factor
    )
    return Organism(offspring_genome)
