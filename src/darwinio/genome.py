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

"""Various methods for encoding and decoding genomes.

Functions:
--------
generate_offspring_genome: Generate a genome_array for an offspring of the given
parents with mutations.
"""

from __future__ import annotations
import random
import numpy as np
import nilsimsa as nil


def generate_offspring_genome(
    parent_1: np.ndarray,
    parent_2: np.ndarray,
    mutation_factor: float,
) -> np.ndarray:
    """Generate a genome_array for an offspring of the given parents with mutations.

    Args:
    -------
    parent_1: The genome of the first parent.

    parent_2: The genome of the second parent.

    mutation_factor: A value between 0 and 1 (inclusive) representing the
    probability of a mutation occurring in the offspring's genome.

    Returns:
    -------
    A string representing the genome of the offspring.

    Notes:
    -------
    The function performs a bit-wise random choice between each base pair of
    the parents' genomes to generate the offspring's genome. If the
    mutation factor is greater than 0, there is a chance for a random mutation
    to occur in one of the offspring's base pairs. The function then returns
    the offspring's genome_array.
    """

    if not 0 <= mutation_factor <= 1:
        raise ValueError(
            "mutation_factor must be a value between 0 and 1 (inclusive)"
        )
    if len(parent_1) != len(parent_2):
        raise ValueError("parent_1 and parent_2 must have the same length")

    # bitwise random choice between each base_pair
    offspring_genome: list = [
        random.choice(base_pair) for base_pair in zip(parent_1, parent_2)
    ]

    # mutations
    if random.random() < mutation_factor:
        random_index: int = random.randrange(len(offspring_genome))
        random_value: int = random.randrange(16**3)
        offspring_genome[random_index] = random_value

    return np.array(offspring_genome)


def array2hex(array: np.ndarray) -> str:
    """Convert array to hex"""
    return nil.Nilsimsa(array.tobytes()).hexdigest()
