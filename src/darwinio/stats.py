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

"""
Classes and related stuff for statistics.
"""
import pandas as pd
import matplotlib.pyplot as plt
from typing import Any


class StatisticsCollector:
    """
    A class for collecting and analyzing statistics.

    Attributes:
    ----------
    data: The DataFrame to store the collected statistics.
    """

    def __init__(self, columns: list[str]):
        """
        Initialize a StatisticsCollector object.

        Args:
        -----
        columns: A list of column names for the data.
        """
        self.data: pd.DataFrame = pd.DataFrame(columns=columns)

    def add(self, new_data: tuple[Any, ...]):
        """
        Add new data to the statistics collector.

        Args:
        -----
        new_data: The new data(row) to be added.
        """
        self.data.loc[len(self.data.index)] = new_data

    def plot(self, columns: list[str]):
        """
        Plot the specified columns of the data.

        Args:
        -----
        columns: A list of column names to be plotted.
        """
        self.data[columns].plot(subplots=True)
        plt.show()

    def clear(self):
        """
        Clear the data in data frame.
        """
        self.data = self.data.iloc[0:0]
