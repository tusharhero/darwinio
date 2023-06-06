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

import pygame as pg
import pygame_gui as pgui


class Slider:
    """A class representing a custom UI element"""

    def __init__(
        self,
        label: str,
        position: tuple[int, int],
        starting_value: int,
        slider_range: tuple[int, int],
        manager: pgui.UIManager,
    ):
        x, y = position
        self.slider = pgui.elements.UIHorizontalSlider(
            pg.Rect(x, y, 400, 30),
            starting_value,
            slider_range,
            manager,
        )
        self.value_label = pgui.elements.UITextBox(
            str(self.slider.get_current_value()),
            pg.Rect(x - 50, y, 50, 60),
            manager,
        )
        self.label = pgui.elements.UITextBox(
            label,
            pg.Rect(x, y + 30, 400, 30),
            manager,
        )

    def update(self):
        self.value_label.set_text(str(self.slider.get_current_value()))
