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

from __future__ import annotations
import distribution
from os import system
from time import sleep

world = distribution.World((30, 30), mutation_factor=0.8)


def create_string_organism(world: distribution.World) -> str:
    return "\n".join(
        [
            " ".join(
                ["O" if organism is not None else " " for organism in row]
            )
            for row in world.organism_distribution
        ]
    )


def print_world(world: distribution.World):
    sleep(0.1)
    system("clear")
    print(create_string_organism(world))


for _ in range(1000):
    print_world(world)
    population = distribution.get_distribution_population(
        world.organism_distribution
    )
    print(f"time:{_} \n  population:{population}")
    world.update_state()
