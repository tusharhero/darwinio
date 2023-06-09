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
"""

import darwinio.brain as brn
import darwinio.genome as gn
import numpy as np


class Organism:
    """A class representing an organism.

    Attributes:
    ---------
    genome_array: A Numpy array representing the organism's genome.

    neural_network: A neural network generated from the genome of the organism
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
    temp_range: tuple[int, int],
    trophic_level_range: tuple[int, int],
    energy_range: tuple[int, int],
    reproductive_types: tuple[int, int],
) -> Organism:
    """Generate a random organism.

    Args:
    -----
    temp_range (Tuple[int, int]): Range of temperature values for the
    organism's adaptation.

    trophic_level_range (Tuple[int, int]): Range of trophic level values for
    the organism's position in the food chain.

    energy_range (Tuple[int, int]): Range of energy values for the organism's
    energy capacity.

    reproductive_types (Tuple[int, int]): Range of reproductive type values for
    the organism's reproductive strategy.

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
    parent_1(np,ndarray): One of the parent Organisms

    parent_2(np,ndarray): One of the parent Organisms

    mutation_factor(int): A value between 0 and 1 (inclusive) representing the
    probability of a mutation occurring in the offspring's genome.

    Returns:
    ---------
    offspring: Child of the parents.
    """
    offspring_genome: np.ndarray = gn.generate_offspring_genome(
        parent_1.genome_array, parent_2.genome_array, mutation_factor
    )
    return Organism(offspring_genome)
