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
Organism class and related stuff.
"""

import random
from brain import NeuralNetwork
import genome as gn
import numpy as np
from typing import Union


class Organism:
    """
    A class representing an organism.

    Note:
    -----------------------------------------------------------------------------------
        characteristics are stored as:
            0: ideal temperature
            1: trophic level
            2: energy requirement
            3: reproductive type

    Attributes:
    -----------------------------------------------------------------------------------
        genome: A string representing the organism's genome.
        characters: A NumPy array containing the organism's characteristics.
        coordinates: A tuple representing the organism's coordinates on a canvas.
        neural_network: A neural network generated from the genome of the organism
    """

    def __init__(
        self,
        input_data: Union[str, np.ndarray],
        canvas_size: tuple[int, int] = (10, 10),
        number_of_characters: int = 4,
    ) -> None:
        """
        Initializes an instance of the Organism class.
        """
        # check if input is genome or characteristics

        if isinstance(input_data, np.ndarray):
            self.genome: str = gn.encode_organism_characteristics(
                input_data, number_of_characters
            )

            self.characters: np.ndarray = input_data

        elif isinstance(input_data, str):
            self.genome: str = input_data
            self.characters: np.ndarray = gn.decode_organism_characteristics(
                input_data, number_of_characters
            )

        # assign random coordinates
        self.canvas_size = canvas_size
        self.coordinates = tuple(
            random.randrange(self.canvas_size[i]) for i in range(2)
        )

        # assign a neural_network generated from the the genome
        self.neural_network = NeuralNetwork(self.genome, np.array([2, 2]))
