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


def get_random_genome(size: int) -> str:
    """randomly generate a genome"""
    return secrets.token_hex(size)


def generate_offspring_genome(parent1: str, parent2: str, mutationfactor: float) -> str:
    """
    Generate a genome for an offspring of the given parents(with mutations).
    mutationfactor must be within [0,1)
    """

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