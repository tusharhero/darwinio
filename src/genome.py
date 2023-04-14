# The GPLv3 License (GPLv3)

# Copyright (c) 2023 Tushar Maharana

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" 
Various methods for encoding and decoding genomes.
"""

import secrets
import random
import numpy as np


def get_random_genome(size: int) -> str:
    """
    Generates a random hexadecimal genome of the specified size.
    """
    return secrets.token_hex(size)


def generate_offspring_genome(parent1: str, parent2: str, mutationfactor: float) -> str:
    """
    Generate a genome for an offspring of the given parents with mutations.

    Args:
    -----------------------------------------------------------------------------------
        parent1: The genome of the first parent.
        parent2: The genome of the second parent.
        mutationfactor: A value between 0 and 1 (inclusive) representing the probability
        of a mutation occurring in the offspring's genome.

    Returns:
    -----------------------------------------------------------------------------------
        A string representing the genome of the offspring.

    Notes:
    -----------------------------------------------------------------------------------
        The function performs a bitwise random choice between each base pair of the parents' genomes
        to generate the offspring's genome. If the mutationfactor is greater than 0, there is a chance
        for a random mutation to occur in one of the offspring's base pairs. The function then returns
        the offspring's genome as a string.
    """

    if not 0 < mutationfactor <= 1:
        raise ValueError("mutationfactor must be a value between 0 and 1 (inclusive)")
    if len(parent1) != len(parent2):
        raise ValueError("parent1 and parent2 must have the same length")

    # bitwise random choice between each base_pair
    offspring_genome: list = [
        random.choice(base_pair) for base_pair in zip(parent1, parent2)
    ]

    # mutations
    if random.random() < mutationfactor:
        random_index: int = random.randrange(len(offspring_genome))
        random_value: str = hex(random.randrange(16))[2:]
        offspring_genome[random_index] = random_value

    return "".join(offspring_genome)


def encode_organism_characteristics(characteristics: np.ndarray, length: int) -> str:
    """
    Encode the given organism characteristics into a genome string.

    Args:
    -----------------------------------------------------------------------------------
        characteristics: A numpy ndarray of integers representing the characteristics
        to be encoded. Each characteristic should be between 0 and 15 (inclusive).
        length: An integer representing length of the genome, if its larger than the
        size of the array, the rest will be generated randomly.

    Returns:
    -----------------------------------------------------------------------------------
        A string representing the genome encoded from the given characteristics. The
        genome is in hexadecimal format, with each characteristic encoded as a pair of
        hexadecimal digits.
    """

    if not isinstance(characteristics, np.ndarray):
        raise TypeError("Characteristics must be a NumPy ndarray")
    if not characteristics.dtype == np.int64:
        raise ValueError("Characteristics must be integers")
    if not np.all((0 <= characteristics) & (characteristics <= 15)):
        raise ValueError("Characteristics must be between 0 and 15 inclusive")
    if not length >= len(characteristics):
        raise ValueError("length must be larger than size of Characteristics")

    genome: list = [hex(character)[2:] for character in characteristics]
    return "".join(genome) + get_random_genome(length - len(characteristics))


def decode_organism_characteristics(genome: str, array_length: int) -> np.ndarray:
    """
    Decode the given genome into an array of organism characteristics.

    Args:
    -----------------------------------------------------------------------------------
        genome:
        The genome string to be decoded.
        array_length:
        The length of the genome, actually intended to contain characteristics

    Returns:
    -----------------------------------------------------------------------------------
        np.ndarray
            A NumPy array containing the decoded organism characteristics. Each
            element of the array represents a characteristic and is an integer
            between 0 and 15.
    """
    if not 0 <= array_length < len(genome):
        raise ValueError("length must be larger than size of Characteristics")
    return np.array([int(base_pair, 16) for base_pair in genome[:array_length]])
