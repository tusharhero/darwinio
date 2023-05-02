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


import distribution
from os import system
from time import sleep

world = distribution.World((30, 30), mutation_factor=0.8)

animal_emojis = {
    "0": "🐵",
    "1": "🐘",
    "2": "🐻",
    "3": "🐦",
    "4": "🐍",
    "5": "🐅",
    "6": "🐊",
    "7": "🐋",
    "8": "🐎",
    "9": "🐘",
    "a": "🦁",
    "b": "🐝",
    "c": "🐫",
    "d": "🐬",
    "e": "🦅",
    "f": "🦊",
}


def create_string_organism(world: distribution.World) -> str:
    return "\n".join(
        [
            " ".join(
                [
                    animal_emojis[organism.genome[:1]]
                    if organism is not None
                    else " "
                    for organism in row
                ]
            )
            for row in world.organism_distribution
        ]
    )


def create_string_food(world: distribution.World) -> str:
    return "\n".join(
        [
            " ".join([str(food) for food in row])
            for row in world.temp_distribution
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
