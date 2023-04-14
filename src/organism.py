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
import genome as gn
import numpy as np
from typing import Union

"""
"""


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
        genome (str): A string representing the organism's genome.
        characters (np.ndarray): A NumPy array containing the organism's characteristics.
        coordinates (tuple[int, int]): A tuple representing the organism's coordinates on a canvas.

    Methods:
    -----------------------------------------------------------------------------------
        __init__(self, input_data, canvas_size=(10, 10))
            Initializes an instance of the Organism class.
    """

    def __init__(
        self,
        input_data: Union[str, np.ndarray],
        canvas_size: tuple[int, int] = (10, 10),
    ) -> None:
        # check if input is genome or characteristics
        if isinstance(input_data, np.ndarray):
            self.genome: str = gn.encode_organism_characteristics(input_data)
            self.characters: np.ndarray = input_data
        elif isinstance(input_data, str):
            self.genome: str = input_data
            self.characters: np.ndarray = gn.decode_organism_characteristics(input_data)

        # assign random coordinates
        self.canvas_size = canvas_size
        self.coordinates = tuple(
            random.randrange(self.canvas_size[i]) for i in range(2)
        )
