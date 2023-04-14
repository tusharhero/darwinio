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
Classes and methods for handling the neural network.
"""

import numpy as np
import genome as gn


class NeuralNetwork:
    """
    A class for representing a neural network with a given genome and neural structure.

    Attributes:
    -----------------------------------------------------------------------------------
        genome: The genome string that encodes the weights of the neural network.
        neuralstructure: A numpy ndarray of integers representing the
        structure of the neural network, where each integer represents the number of
        neurons in that layer.
        weights: contains weights of the neural network.
    """

    def __init__(self, genome: str, neuralstructure: np.ndarray) -> None:
        """
        Initialize a neural network object with the given genome and neural structure.

        Args:
        ----------------------------------------------------------------------
        genome: A string representing the genome of the organism.
        neuralstructure: A numpy ndarray representing the neural structure of the organism.

        Raises:
        ----------------------------------------------------------------------
        ValueError: If the genome is not large enough for the given neural structure.
        """
        self.genome: str = genome
        self.neuralstructure: np.ndarray = neuralstructure
        self.create_weights()

    def create_weights(self) -> None:
        """
        Creates the weights for the neural network based on the genome and neural structure.

        Raises:
        ----------------------------------------------------------------------
        ValueError: If the genome is not large enough for the given neural structure.
        """

        neuralstructure: np.ndarray = self.neuralstructure

        number_of_neural_connections: int = int(
            np.sum(neuralstructure[:-1] * neuralstructure[1:])
        )

        genome_seq: np.ndarray = gn.decode_organism_characteristics(
            self.genome, len(self.genome)
        )

        length_of_genome: int = len(genome_seq)
        length_of_neural_section: int = length_of_genome // number_of_neural_connections

        if not length_of_neural_section > 0:
            raise ValueError("Genome is not large enough.")

        # generate the weights
        weights: np.ndarray = np.array(
            [
                np.sum(
                    genome_seq[
                        i
                        * length_of_neural_section : (i + 1)
                        * length_of_neural_section
                    ]
                )
                for i in range(number_of_neural_connections)
            ]
        )

        # normalize to the range [-0.5, 0.5]
        weights: np.ndarray = (weights / (15 * length_of_neural_section)) - 0.5

        self.weights: np.ndarray = weights
