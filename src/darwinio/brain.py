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

"""Classes and methods for handling the neural network.

Classes:
-------------
NeuralNetwork: A class for representing a neural network with a given genome
and neural structure.

Functions:
-------------
create_weights: Creates the weights for the neural network based on the
genome and neural structure.

normalize_array: Creates the weights for the neural network based on the genome
and neural structure.
"""

from __future__ import annotations
import numpy as np


class NeuralNetwork:
    """A class for representing a neural network with a given genome and neural
    structure.

    Attributes:
    ----------
    weights: contains weights of the neural network.

    neural_structure: A numpy ndarray of integers representing the structure of
    the neural network, where each integer represents the number of neurons in
    that layer.
    """

    def __init__(
        self, weights: np.ndarray, neural_structure: np.ndarray
    ) -> None:
        """Initialize a neural network object with the given weight and neural
        structure.

        Args:
        -----
        weights: An one-dimensional Numpy Array containing the weights for
        the neural network.

        neural_structure: An one-dimensional Numpy Array representing the
        neural structure of the organism.
        """

        self.weights: np.ndarray = weights
        self.neural_structure: np.ndarray = neural_structure

    def run_neural_network(self, input_values: np.ndarray) -> np.ndarray:
        """Run the neural network according to input values.

        Args:
        -----
        input_values: A numpy ndarray representing the input values of the
        neural network.

        Returns:
        --------
        A numpy ndarray with the output values of the neural network

        Note:
        -----
        This method runs the neural network with the given input values using
        the current weights and neural structure of the neural network. It
        initializes a new empty neural network and fills in the values using
        the provided input and the weights. The weights are then applied to the
        corresponding input neuron to obtain the output of the next neuron in
        the network. The output of each layer is passed through the activation
        function (tanh) and stored in the neural network list. Finally, the
        output of the last layer is returned as a Numpy Array.
        """

        normalized_input_values: np.ndarray = normalize(input_values)
        weights: np.ndarray = self.weights
        neural_structure: np.ndarray = self.neural_structure
        neural_network: list[list[float]] = [
            [0.0] * i for i in neural_structure
        ]

        neural_network[0] = list(normalized_input_values)

        for layer_index in range(len(neural_network[:-1])):
            layer_values = neural_network[layer_index]
            next_layer_index = layer_index + 1

            # calculate the dot product between the current layer and the
            # weights for the next layer
            next_layer_values = np.dot(
                layer_values,
                weights[
                    : len(layer_values) * len(neural_network[next_layer_index])
                ].reshape(
                    len(layer_values), len(neural_network[next_layer_index])
                ),
            )

            # reshape the resulting values to match the shape of the next layer
            next_layer_values = next_layer_values.reshape(
                len(neural_network[next_layer_index]),
            )
            # apply the activation function to the next layer values

            next_layer_values = np.tanh(next_layer_values)
            neural_network[next_layer_index] = list(next_layer_values)

        return np.array(neural_network[-1])


def normalize(arr: np.ndarray) -> np.ndarray:
    """Normalize the Numpy Array."""
    magnitude: np.floating = np.linalg.norm(arr) + 1e-16
    return arr / magnitude


def create_weights(
    genome_array: np.ndarray, neural_structure: np.ndarray
) -> np.ndarray:
    """Creates the weights for the neural network based on the genome and
    neural structure.

    Args:
    -----
    genome_array: A Numpy Array representing the hexadecimal genome of the organism.

    neural_structure: A Numpy Array representing the structure of the neural network.

    Returns:
    -------
    A Numpy Array containing the weights.
    """

    number_of_neural_connections = int(
        np.sum(neural_structure[:-1] * neural_structure[1:])
    )

    # generate the weights
    weights: np.ndarray = genome_array[:number_of_neural_connections]

    # normalize to the range [-1, 1]
    weights: np.ndarray = normalize(weights)

    return weights
