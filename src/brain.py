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

"""
Classes and methods for handling the neural network.

Classes:
-------------
    NeuralNetwork: A class for representing a neural network with a given genome and neural structure.

Methods:
-------------
    create_weights: Creates the weights for the neural network based on the genome and neural structure.

    run_neural_network: Runs the neural network according to input values.
"""

import numpy as np
import genome as gn


class NeuralNetwork:
    """
    A class for representing a neural network with a given genome and neural structure.

    Args:
    -----
        genome: A string representing the genome of the organism.

        neural_structure: A numpy ndarray representing the neural structure
        of the organism.

    Attributes:
    -----
        genome: The genome string that encodes the weights of the neural network.

        neural_structure: A numpy ndarray of integers representing the
        structure of the neural network, where each integer represents the number of
        neurons in that layer.

        weights: contains weights of the neural network.
    """

    def __init__(self, genome: str, neural_structure: np.ndarray) -> None:
        """
        Initialize a neural network object with the given genome and
        neural structure.

        Args:
        -----
        genome: A string representing the genome of the organism.

        neural_structure: A numpy ndarray representing the neural structure of
        the organism.

        Raises:
        -----
        ValueError: If the genome is not large enough for the given neural structure.
        """
        self.genome: str = genome
        self.neural_structure: np.ndarray = neural_structure
        self.create_weights()

    def create_weights(self) -> None:
        """
        Creates the weights for the neural network based on the genome and
        neural structure.

        Raises:
        -----
        ValueError: If the genome is not large enough for the given neural structure.
        """

        neural_structure: np.ndarray = self.neural_structure

        number_of_neural_connections = int(
            np.sum(neural_structure[:-1] * neural_structure[1:])
        )

        genome_seq: np.ndarray = gn.decode_organism_characteristics(
            self.genome, len(self.genome)
        )

        length_of_genome = len(genome_seq)
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

    def run_neural_network(self, input_values: np.ndarray) -> np.ndarray:
        """
        Run the neural network according to input values.

        Args:
        -----
        input_values: A numpy ndarray representing the input values of the neural network.

        Returns:
        -----
        A numpy ndarray with the output values of the neural network

        Note:
        -----
        The method uses the current weights and neural structure of the neural network to calculate
        the output values based on the given input values. It does this by initializing a new
        empty neural network and filling in the values using the provided input and the weights.
        The weights are applied to the corresponding input neuron to obtain the output of the next
        neuron in the network. Finally, the output of the last layer is returned as a numpy ndarray.
        """

        weights: np.ndarray = self.weights
        neural_structure: np.ndarray = self.neural_structure
        neural_network: list[list[float]] = [[0.0] * i for i in neural_structure]

        neural_network[0] = list(input_values)

        weight_index = 0
        for layer_index, layer_values in enumerate(neural_network[:-1]):
            next_layer_index = layer_index + 1
            for neuron_value in layer_values:
                for next_layer_neuron_index, next_layer_neuron_value in enumerate(
                    neural_network[next_layer_index]
                ):
                    neural_network[next_layer_index][next_layer_neuron_index] = (
                        next_layer_neuron_value + weights[weight_index] * neuron_value
                    )
                    weight_index += 1

        return np.array(neural_network[-1])
