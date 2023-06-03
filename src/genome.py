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
get_random_genome: a random hexadecimal genome of the specified size.

generate_offspring_genome: Generate a genome for an offspring of the given
parents with mutations.

encode_organism_characters: Encode the given organism characters
into a genome string.

decode_organism_characters: Decode the given genome into an array of
organism characters.
"""

import random
import numpy as np


def get_random_genome(size: int) -> str:
    """Generates a random hexadecimal genome of the specified size."""
    return "".join(
        [random.choice("0123456789abcdef") for _ in range(size if size >= 0 else 0)]
    )


def generate_basepairs(genome: str, letters_per_character: int) -> np.ndarray:
    """Convert a genome string into an array of base pairs.

    Args:
    -------
    genome: A string representing the genome to be converted.

    letters_per_character: The number of characters in the genome string that
    should be combined to form each base pair.

    Returns:
    -------
    A NumPy array of strings representing the base pairs in the genome.

    The function first splits the genome string into substrings of length
    letters_per_character the resulting strings are then returned as a NumPy
    array of base pairs.
    """
    return np.array(
        [
            "".join(genome[i : i + letters_per_character])
            for i in range(0, len(genome), letters_per_character)
        ]
    )


def generate_offspring_genome(
    parent_1: str,
    parent_2: str,
    mutation_factor: float,
    letters_per_character: int = 1,
) -> str:
    """Generate a genome for an offspring of the given parents with mutations.

    Args:
    -------
    parent_1: The genome of the first parent.

    parent_2: The genome of the second parent.

    mutation_factor: A value between 0 and 1 (inclusive) representing the
    probability of a mutation occurring in the offspring's genome.

    letters_per_character: The amount of digits used for representing each
    character.

    Returns:
    -------
    A string representing the genome of the offspring.

    Notes:
    -------
    The function performs a bitwise random choice between each base pair of
    the parents' genomes to generate the offspring's genome. If the
    mutationfactor is greater than 0, there is a chance for a random mutation
    to occur in one of the offspring's base pairs. The function then returns
    the offspring's genome as a string.
    """

    if not 0 <= mutation_factor <= 1:
        raise ValueError("mutation_factor must be a value between 0 and 1 (inclusive)")
    if len(parent_1) != len(parent_2):
        raise ValueError("parent_1 and parent_2 must have the same length")

    # generate basepairs
    parent_1_basepairs = generate_basepairs(parent_1, letters_per_character)
    parent_2_basepairs = generate_basepairs(parent_2, letters_per_character)

    # bitwise random choice between each base_pair
    offspring_genome: list = [
        random.choice(base_pair)
        for base_pair in zip(parent_1_basepairs, parent_2_basepairs)
    ]

    # mutations
    if random.random() < mutation_factor:
        random_index: int = random.randrange(len(offspring_genome))
        random_value: str = hex(random.randrange(16))[2:]
        offspring_genome[random_index] = random_value

    return "".join(offspring_genome)


def encode_organism_characters(
    characters: np.ndarray, length: int, letters_per_character: int = 1
) -> str:
    """Encode the given organism characters into a genome string.

    Args:
    -------
    characters: A numpy ndarray of integers representing the
    characters to be encoded.

    length: An integer representing length of the genome, if it's larger than
    the size of the array, the rest will be generated randomly.

    letters_per_character: The amount of digits used for representing each
    character.

    Returns:
    -------
    A string representing the genome encoded from the given characters.
    The genome is in hexadecimal format, with each characteristic encoded as
    hexadecimal digits.
    """

    # check for errors
    if not isinstance(characters, np.ndarray):
        raise TypeError("Characters must be a NumPy ndarray")
    if not characters.dtype == np.int64:
        raise ValueError("Characters must be integers")
    if not np.all((0 <= characters) & (characters <= 16**letters_per_character)):
        raise ValueError(
            f"Characters must be between 0 and {16**letters_per_character -1}inclusive"
        )
    if not length >= len(characters):
        raise ValueError("length must be larger than size of Characters")

    hex_characters = [hex(character)[2:] for character in characters]

    genome_list: list = [
        "0" * (letters_per_character - len(character)) + character
        for character in hex_characters
    ]

    return "".join(genome_list) + get_random_genome(length - len(characters))


def decode_organism_characters(
    genome: str, array_length: int, letters_per_character: int = 1
) -> np.ndarray:
    """Decode the given genome into an array of organism characters.

    Args:
    -------
    genome: The genome string to be decoded.

    array_length: The length of the genome, actually intended to contain
    characters

    letters_per_character: The amount of digits used for representing each
    character.

    Returns:
    -------
    A NumPy array containing the decoded organism characters. Each
    element of the array represents a characteristic and is an integer
    between 0 and 16**letters_per_character-1.
    """

    if not 0 <= array_length <= len(genome):
        raise ValueError("length must be larger than size of Characters")

    return np.array(
        [
            int(base_pair, 16)
            for base_pair in generate_basepairs(genome, letters_per_character)
        ]
    )
