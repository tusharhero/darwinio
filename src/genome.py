"""
The GPLv3 License (GPLv3)

Copyright (c) 2023 Tushar Maharana

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

""" 
Various methods for encoding and decoding genomes.
"""

import secrets
import random


def get_random_genome(size: int) -> str:  # randomly generate a genome
    return secrets.token_hex(size)


def get_offspring_genome(parent1: str, parent2: str, mutationfactor: float) -> str:
    # bitwise random choice between each bp
    offspring_genome: list = [random.choice(bp) for bp in zip(parent1, parent2)]

    # mutations
    if random.choices([True, False], [mutationfactor, 1 - mutationfactor])[0]:
        offspring_genome[random.randrange(len(offspring_genome))] = random.choice(
            offspring_genome
        )
    return "".join(offspring_genome)
