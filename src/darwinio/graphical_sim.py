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

from __future__ import annotations

import copy
from importlib.metadata import Distribution
import threading
from importlib.resources import as_file, files
from typing import Any, Union, Tuple
import math

import pygame as pg
import pygame_gui as pgui
import numpy as np

import darwinio.distribution as dist
import darwinio.organism as org
import darwinio.genome as gn
import darwinio.stats as statistics


class World(dist.World):
    """Represents a world in which organisms and food are distributed across a
    canvas.

    An additional method to render the world.
    """

    def render(self, surface: pg.Surface, images: list[pg.Surface]):
        """
        Renders the organisms on the given surface using the provided image.

        Args:
        -----
        surface: The surface on which the organisms will be rendered.

        images: The images representing organisms.
        """
        organisms = self.organism_distribution.data
        for y, row in enumerate(organisms):
            for x, organism in enumerate(row):
                if organism is not None:
                    image = images[
                        np.clip(
                            int(organism.get_tier() * len(images)), 0, len(images) - 1
                        )
                    ]
                    color = pg.Color(f"#{gn.array2hex(organism.genome_array)[-6:]}")
                    tinted_image: pg.Surface = tint(image, color)
                    surface.blit(tinted_image, (x * 64, y * 64))


def render_np_2d_array(array: np.ndarray, surface: pg.Surface):
    """
    Renders the NumPy array on the given surface.

    Args:
    -----
    array: The NumPy array to be rendered.

    surface: The surface on which the NumPy array will be rendered.
    """
    color_pixel_size = size_x, size_y = tuple(
        surface.get_size()[_] / array.shape[_] for _ in range(2)
    )
    color_pixel: pg.Surface = pg.Surface(color_pixel_size)
    max_value: int = array.max()
    min_value: int = array.min()
    for y, row in enumerate(array):
        for x, datapoint in enumerate(row):
            color_brightness: int = round(
                255 * (datapoint - min_value) / (max_value - min_value)
                if max_value - min_value != 0
                else 0
            )

            # https://krazydad.com/tutorials/makecolors.php

            r = round(math.sin(0.01 * color_brightness + 0 * math.pi / 3) * 127 + 128)
            g = round(math.sin(0.01 * color_brightness + 1 * math.pi / 3) * 127 + 128)
            b = round(math.sin(0.01 * color_brightness + 2 * math.pi / 3) * 127 + 128)

            color: Tuple[int, int, int] = (r, g, b)

            color_pixel.fill(color)
            surface.blit(color_pixel, (size_x * x, size_y * y))


class State:
    """
    Represents a game
    state.

    Attributes:
    -----------
    manager: The UI manager for the state.

    surface: The surface on which the state is rendered.

    next_state_index: The index of the next state
    """

    def __init__(
        self,
        surface: pg.Surface,
        manager_size: tuple[int, int],
        next_state_index: Union[int, None],
    ):
        """
        Args:
        ------
        surface: The surface on which the state will be rendered.

        initial_manager_size: The initial size of the UI manager.

        next_state_index: The index of the next state
        """
        self.next_state_index: Union[int, None] = next_state_index
        self.manager = pgui.UIManager(manager_size)
        self.surface: pg.Surface = surface

    def render(self):
        """Render the state."""
        self.manager.draw_ui(self.surface)

    def update(self, events: list[pg.Event], time_delta: float) -> Union[int, None]:
        """
        Update the state.

        Args:
        ------
        events: The list of pygame events.

        time_delta: The time elapsed since the last update.

        Returns:
        --------
        None: if the state is not changing, Or the the index of the next
        scene.
        """
        for event in events:
            self.manager.process_events(event)
        self.manager.update(time_delta)
        return None


class StateMachine:
    """
    Represents a state machine that manages a collection of states.


    Attributes:
    -----------
    states: The list of states in the state machine.

    state_index: The index of the current active state.
    """

    def __init__(self, states: list[State]):
        """
        Initialize the StateMachine object.

        Args:
        -----
        states: The list of states in the state machine.
        """
        self.states: list[State] = states
        self.state_index: int = 0

    def run_state(self, events: list[pg.Event], time_delta: float):
        """
        Run the current active state in the state machine.

        Args:
        -----
        events: The list of pygame events.

        time_delta: The time elapsed since the last update.
        """
        state: State = self.states[self.state_index]
        state.render()
        new_state_index: Union[int, None] = state.update(events, time_delta)
        self.state_index = (
            new_state_index if new_state_index is not None else self.state_index
        )


class Slider:
    """A class representing a custom UI element"""

    def __init__(
        self,
        label: str,
        position: tuple[int, int],
        initial_value: int,
        slider_range: tuple[int, int],
        manager: pgui.UIManager,
    ):
        """
        Args:
        -----
        label: text to be displayed on the label.

        position: position of the slider.

        initial_value: initial value of the sliding bar.

        slider_range: range of the values that the slider is allowed to get
        into.
        """
        x, y = position
        self.slider = pgui.elements.UIHorizontalSlider(
            pg.Rect(x, y, 400, 30),
            initial_value,
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
        """
        Update the value label.
        """
        self.value_label.set_text(str(self.slider.get_current_value()))


class OrganismSelection(State):
    """Represents a organism criteria selection screen."""

    def __init__(
        self,
        surface: pg.Surface,
        world: World,
        next_state_index: Union[int, None],
    ):
        surface_size = width, height = surface.get_size()
        super().__init__(surface, surface_size, next_state_index)
        self.world: World = world

        self.title = pgui.elements.UITextBox(
            "Select how you want to your organisms to initally spawn.",
            pg.Rect((width // 2) - 350 // 2, 50, 350, 70),
            self.manager,
        )

        self.energy_slider_min = Slider(
            "Food min:", (350, 150), 100, (1, 2000), self.manager
        )
        self.energy_slider_max = Slider(
            "Food max:", (350, 250), 1000, (1, 2000), self.manager
        )

        self.temp_slider_min = Slider(
            "Temp min:", (350, 350), 30, (1, 2000), self.manager
        )
        self.temp_slider_max = Slider(
            "Temp max:", (350, 450), 150, (1, 2000), self.manager
        )

        self.done_button = pgui.elements.UIButton(
            pg.Rect(0, 550, -1, -1),
            "Done!",
            self.manager,
            anchors={"centerx": "centerx"},
        )
        self.skip_button = pgui.elements.UIButton(
            pg.Rect(0, 600, -1, -1),
            "skip",
            self.manager,
            anchors={"centerx": "centerx"},
        )
        self.painting_distribution_button = pgui.elements.UIButton(
            pg.Rect(0, 650, -1, -1),
            "customize the other distributions.",
            self.manager,
            anchors={"centerx": "centerx"},
        )

    def update(self, events: list[pg.Event], time_delta: float) -> Union[int, None]:
        """
        Updates the state based on the given events and time delta.

        Args:
        -----
        events: A list of Pygame events.

        time_delta: The time difference between the current and previous frame.
        """
        for event in events:
            if event.type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == self.done_button:
                    energy_range: tuple[int, int] = (
                        int(self.energy_slider_min.slider.get_current_value()),
                        int(self.energy_slider_max.slider.get_current_value()),
                    )
                    temp_range: tuple[int, int] = (
                        int(self.temp_slider_min.slider.get_current_value()),
                        int(self.temp_slider_max.slider.get_current_value()),
                    )

                    org.Organism.energy_range = energy_range
                    org.Organism.temp_range = temp_range

                    self.world.organism_distribution = (
                        dist.OrganismDistribution.generate(size=self.world.canvas_size)
                    )
                    return self.next_state_index
                if event.ui_element == self.skip_button:
                    return self.next_state_index
                if event.ui_element == self.painting_distribution_button:
                    return -1
            self.manager.process_events(event)

        self.energy_slider_max.update()
        self.energy_slider_min.update()
        self.temp_slider_max.update()
        self.temp_slider_min.update()

        self.manager.update(time_delta)
        return None


class DistributionPainting(State):
    """Represents a distribution painting screen."""

    def __init__(
        self,
        surface: pg.Surface,
        world: World,
        next_state_index: Union[int, None],
    ):
        self.surface_size = width, height = surface.get_size()
        super().__init__(surface, self.surface_size, next_state_index)
        self.world: World = world

        self.canvas_surface: pg.Surface = pg.Surface((500, 500))
        self.canvas_rect: pg.Rect = self.canvas_surface.get_rect(
            center=(width // 2, height // 2)
        )
        self.canvas_offset: Tuple[int, int] = self.canvas_rect.topleft

        self.distribution_labels = {
            self.world.food_distribution: "Food distribution",
            self.world.temp_distribution: "Temperature distribution",
        }

        # State variables
        self.current_distribution: dist.Distribution = self.world.temp_distribution

        # User interface variables
        self.title = pgui.elements.UITextBox(
            "<b>Customize the distributions.</b>",
            pg.Rect((width // 2) - 350 // 2, 20, 350, -1),
            self.manager,
        )
        self.current_distribution_label_text: str = (
            f"<b>Customizing {self.distribution_labels[self.current_distribution]}</b>"
        )

        self.current_distribution_label = pgui.elements.UITextBox(
            self.current_distribution_label_text,
            pg.Rect((width // 2) - 350 // 2, 60, 350, -1),
            self.manager,
        )

        self.instrument: str = "paintbrush"

        self.instrument_indicator = pgui.elements.UITextBox(
            self.instrument, pg.Rect(width - 90, 150, 100, -1), self.manager
        )
        self.paint_button = pgui.elements.UIButton(
            pg.Rect(width - 70, 80, -1, -1), "paint", self.manager
        )
        self.eraser_button = pgui.elements.UIButton(
            pg.Rect(width - 70, 120, -1, -1), "eraser", self.manager
        )

        self.clear_canvas_button = pgui.elements.UIButton(
            pg.Rect(width - 150, 210, -1, -1), "clear the canvas", self.manager
        )
        self.temp_heatmap_button = pgui.elements.UIButton(
            pg.Rect(0, 80, -1, -1), "temp", self.manager
        )
        self.food_heatmap_button = pgui.elements.UIButton(
            pg.Rect(0, 120, -1, -1), "food", self.manager
        )

        self.current_distribution_min_label = pgui.elements.UITextBox(
            f"min: {self.current_distribution.data.min()}",
            pg.Rect(width - 130, 300, -1, -1),
            self.manager,
        )
        self.current_distribution_max_label = pgui.elements.UITextBox(
            f"max: {self.current_distribution.data.max()}",
            pg.Rect(width - 130, 360, -1, -1),
            self.manager,
        )
        self.done_button = pgui.elements.UIButton(
            pg.Rect(0, 650, -1, -1),
            "Done!",
            self.manager,
            anchors={"centerx": "centerx"},
        )

    def render(self):
        render_np_2d_array(self.current_distribution.data, self.canvas_surface)
        self.surface.blit(self.canvas_surface, self.canvas_rect)
        super().render()

    def update(self, events: list[pg.Event], time_delta: float) -> Union[int, None]:
        """
        Updates the state based on the given events and time delta.

        Args:
        -----
        events: A list of Pygame events.

        time_delta: The time difference between the current and previous frame.
        """
        width, height = self.surface_size
        canvas_width, canvas_height = self.canvas_surface.get_size()
        mouse_pos = pg.mouse.get_pos()
        mouse_canvas_pos: Tuple[int, ...] = tuple(
            mouse_pos[_] - self.canvas_offset[_] for _ in range(2)
        )
        mouse_x_rel, mouse_y_rel = mouse_canvas_pos
        is_mouse_in_canvas: bool = (0 < mouse_x_rel < canvas_width) and (
            0 < mouse_y_rel < canvas_height
        )

        if pg.mouse.get_pressed()[0] and is_mouse_in_canvas:
            x_index, y_index = mouse_x_rel // 10, mouse_y_rel // 10
            self.current_distribution.data[y_index][x_index] += (
                100 if self.instrument == "paintbrush" else -100
            )

            self.current_distribution_min_label = pgui.elements.UITextBox(
                f"min: {self.current_distribution.data.min()}",
                pg.Rect(width - 130, 300, -1, -1),
                self.manager,
            )
            self.current_distribution_max_label = pgui.elements.UITextBox(
                f"max: {self.current_distribution.data.max()}",
                pg.Rect(width - 130, 360, -1, -1),
                self.manager,
            )

        for event in events:
            if event.type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == self.done_button:
                    return self.next_state_index
                if event.ui_element == self.temp_heatmap_button:
                    self.current_distribution = self.world.temp_distribution
                if event.ui_element == self.food_heatmap_button:
                    self.current_distribution = self.world.food_distribution

                if event.ui_element == self.paint_button:
                    self.instrument = "paintbrush"
                if event.ui_element == self.eraser_button:
                    self.instrument = "eraser"

                if event.ui_element == self.clear_canvas_button:
                    self.current_distribution.data = np.zeros(
                        shape=self.current_distribution.data.shape
                    )

                if event.ui_element == self.done_button:
                    return self.next_state_index

                self.instrument_indicator = pgui.elements.UITextBox(
                    self.instrument, pg.Rect(width - 90, 150, 100, -1), self.manager
                )
                self.current_distribution_label_text = (
                    f"<b>Customizing {self.distribution_labels[self.current_distribution]}</b>"
                )  # fmt: skip
                self.current_distribution_label = pgui.elements.UITextBox(
                    self.current_distribution_label_text,
                    pg.Rect((width // 2) - 350 // 2, 60, 350, -1),
                    self.manager,
                )

        return super().update(events, time_delta)


class Simulation(State):
    """Represents the main screen state of the game."""

    def __init__(
        self,
        surface: pg.Surface,
        world: World,
        stats: statistics.StatisticsCollector,
        images: list[pg.Surface],
    ):
        """
        Args:
        -----
        surface: The surface on which the state will be rendered.

        world: The world object containing the simulation data.

        stats: The stats object for collecting data and plotting.

        images: The images representing organisms.
        """

        surface_size = width, height = surface.get_size()
        super().__init__(surface, surface_size, None)

        # Simulation Interface

        self.images: list[pg.Surface] = images

        self.running = False

        self.world: World = world
        self.world_buffer = copy.deepcopy(self.world)
        self.thread = threading.Thread(target=self.world.update_state)
        world_width, world_height = world.canvas_size
        self.world_surface: pg.Surface = pg.surface.Surface(
            (world_height * 64, world_width * 64)
        )
        self.world_rect: pg.Rect = self.world_surface.get_rect(
            center=(width // 2, height // 2)
        )
        self.world_scale: float = 1.0
        self.scaled_world_surface: pg.Surface = self.world_surface

        self.sim_surface: pg.Surface = pg.surface.Surface((width, height))
        self.sim_rect: pg.Rect = self.sim_surface.get_rect(
            center=(width // 2, height // 2)
        )

        self.last_time = 0

        # User Interface
        self.start_button = pgui.elements.UIButton(
            pg.Rect(width - 100, height - 30, 100, 30), "start", self.manager
        )
        self.restart_button = pgui.elements.UIButton(
            pg.Rect(width - 100, height - 60, 100, 30), "restart", self.manager
        )
        self.graph_viz_button = pgui.elements.UIButton(
            pg.Rect(0, 40, -1, -1), "graph", self.manager
        )
        self.temp_heatmap_button = pgui.elements.UIButton(
            pg.Rect(0, 80, -1, -1), "temp", self.manager
        )
        self.food_heatmap_button = pgui.elements.UIButton(
            pg.Rect(0, 120, -1, -1), "food", self.manager
        )
        self.population_label = pgui.elements.UITextBox(
            "0", pg.Rect(0, 0, -1, -1), self.manager
        )
        self.temp_slider = Slider(
            "adjust temperature",
            (width - 500, height - 60),
            45,
            (0, 500),
            self.manager,
        )
        self.food_slider = Slider(
            "adjust the food content",
            (width - 950, height - 60),
            500,
            (0, 1200),
            self.manager,
        )

        # Stats
        self.stats: statistics.StatisticsCollector = stats

    def render(self) -> None:
        """render the main screen state."""
        self.sim_surface.fill("black")
        self.world_surface.fill("#5498C6")
        self.world_buffer.render(self.world_surface, self.images)
        self.sim_surface.blit(self.scaled_world_surface, self.world_rect)
        self.surface.blit(self.sim_surface, self.sim_rect)
        self.manager.draw_ui(self.surface)

    def update(self, events: list[pg.Event], time_delta: float) -> Union[int, None]:
        for event in events:
            if event.type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    self.running = not self.running
                    self.last_time = 0
                if event.ui_element == self.restart_button:
                    self.running = False
                    self.stats.clear()
                    return 4

                # graph buttons
                if (
                    event.ui_element == self.graph_viz_button
                    and not self.stats.data.empty
                ):
                    self.stats.plot(
                        ["Population", "Food", "Temperature", "Reproduction Ratio"],
                        "Variables plot",
                    )
                if event.ui_element == self.temp_heatmap_button:
                    statistics.plot_heatmap(
                        self.world.temp_distribution.data,
                        "Temperature distribution",
                    )
                if event.ui_element == self.food_heatmap_button:
                    statistics.plot_heatmap(
                        self.world.food_distribution.data,
                        "Food distribution",
                    )
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.running = not self.running
                    self.last_time = 0

            # change the temp/food content
            if event.type == pgui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.temp_slider.slider:
                    new_avg_temp = self.temp_slider.slider.get_current_value()
                    self.world.temp_distribution = dist.Distribution.generate(
                        self.world.canvas_size, int(new_avg_temp), 50
                    )
                    self.temp_slider.update()
                if event.ui_element == self.food_slider.slider:
                    new_avg_food_content = self.food_slider.slider.get_current_value()
                    self.world.food_distribution = dist.Distribution.generate(
                        self.world.canvas_size, int(new_avg_food_content), 100
                    )
                    self.food_slider.update()

            self.manager.process_events(event)

        keys_pressed = pg.key.get_pressed()
        # moving
        step_size: int = 500
        if keys_pressed[pg.K_UP] or keys_pressed[pg.K_k]:
            self.world_rect.centery += int(step_size * time_delta)
        if keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_j]:
            self.world_rect.centery -= int(step_size * time_delta)
        if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_l]:
            self.world_rect.centerx -= int(step_size * time_delta)
        if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_h]:
            self.world_rect.centerx += int(step_size * time_delta)

        # can't move beyond
        wiggle_room: int = 100
        if self.world_rect.top > self.sim_rect.top + wiggle_room:
            self.world_rect.top = self.sim_rect.top + wiggle_room
        if self.world_rect.bottom < self.sim_rect.bottom - wiggle_room:
            self.world_rect.bottom = self.sim_rect.bottom - wiggle_room
        if self.world_rect.left > self.sim_rect.left + wiggle_room:
            self.world_rect.left = self.sim_rect.left + wiggle_room
        if self.world_rect.right < self.sim_rect.right - wiggle_room:
            self.world_rect.right = self.sim_rect.right - wiggle_room

        # zooming
        scaling: float = 0.5
        if keys_pressed[pg.K_EQUALS] and self.world_scale < 2:
            self.world_scale += scaling * time_delta
        if keys_pressed[pg.K_MINUS] and self.world_scale > 0.5:
            self.world_scale -= scaling * time_delta

        self.scaled_world_surface = pg.transform.scale_by(
            self.world_surface, self.world_scale
        )
        self.world_rect = self.scaled_world_surface.get_rect(
            center=self.world_rect.center
        )

        if self.running:
            self.start_button.set_text("running")
        else:
            self.start_button.set_text("start")

        # run every 1000 milliseconds
        self.update_sim(1000)

        self.population_label.set_text(
            str(self.world.organism_distribution.get_population())
        )

        self.manager.update(time_delta)
        return None

    def update_sim(self, cycle_time_ms: int):
        """
        for updating the world.

        Args:
        -----
        cycle_time_ms: cycle time under which the world would be updated once
        in milliseconds.
        """
        current_time = pg.time.get_ticks()
        if (
            current_time - self.last_time > cycle_time_ms
            and self.running
            and not self.thread.is_alive()
        ):
            self.world_buffer = copy.deepcopy(self.world)
            self.thread = threading.Thread(target=self.world.update_state)
            self.last_time = current_time
            self.thread.start()
            self.stats.add(
                (
                    self.world.organism_distribution.get_population(),
                    self.world.food_distribution.data.mean(),
                    self.world.temp_distribution.data.mean(),
                    self.world.organism_distribution.get_reproduction_ratio(),
                )
            )


class TitleScreen(State):
    """
    Represents the title screen state of the game.

    Attributes:
    -----------
    font: The font used for rendering the title.

    title_surf: The rendered title surface.

    surface: The surface on which the state is rendered.
    """

    def __init__(
        self,
        surface: pg.Surface,
        title_text: str,
        subtitle_text: str,
        next_state_index: int,
    ) -> None:
        """
        Args:
        -----
        surface: The surface on which the state will be rendered.

        title_text: The text to be displayed as the title.

        subtitle_text: The text to be displayed as the subtitle.

        next_state_index: The index of the next state
        """

        font: pg.Font = pg.font.SysFont("monospace", 25)
        self.title_surf: pg.Surface = font.render(title_text, True, "white")

        smallerfont: pg.Font = pg.font.SysFont("monospace", 12)
        self.subtitle_surf: pg.Surface = smallerfont.render(
            subtitle_text, True, "white"
        )

        self.surface: pg.Surface = surface

        self.next_state_index = next_state_index

    def render(self) -> None:
        """Render the title screen state."""
        self.title_surf = pg.transform.scale(
            self.title_surf,
            (self.surface.get_width(), self.title_surf.get_height()),
        )
        titlerect = self.title_surf.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(self.title_surf, titlerect)

        subtitlerect = self.subtitle_surf.get_rect(
            center=self.surface.get_rect().center
        )
        subtitlerect.centery += 200
        self.surface.blit(self.subtitle_surf, subtitlerect)

    def update(self, events: list[pg.Event], time_delta: float) -> Union[int, None]:
        """
        Update the title screen state.

        Args:
        -----
        events: The list of pygame events.

        time_delta: The time elapsed since the last update.

        Returns:
        -------
        int: The index of the next state to transition to, or None if no
        transition is needed.
        """
        for event in events:
            if event.type == pg.KEYDOWN and event.key != pg.K_F11:
                return self.next_state_index
        return None


class HeadingTextScreen(TitleScreen):
    def __init__(
        self,
        surface: pg.Surface,
        title_text: str,
        content_text: str,
        next_state_index: int,
    ) -> None:
        """
        Args:
        -----
        surface: The surface on which the state will be rendered.

        title_text: The text to be displayed as the title.

        content_text: The text to be displayed as the content.

        next_state_index: The index of the next state
        """

        font: pg.Font = pg.font.SysFont("monospace", 100)
        self.title_surf: pg.Surface = font.render(title_text, True, "white")

        smallerfont: pg.Font = pg.font.SysFont("monospace", 30)
        self.content_text_surf: pg.Surface = smallerfont.render(
            content_text, True, "white"
        )

        self.surface: pg.Surface = surface

        self.next_state_index = next_state_index

    def render(self) -> None:
        """Render the text screen state."""

        titlerect = self.title_surf.get_rect(midtop=self.surface.get_rect().midtop)
        titlerect = self.title_surf.get_rect(midtop=self.surface.get_rect().midtop)
        self.surface.blit(self.title_surf, titlerect)

        subtitlerect = self.content_text_surf.get_rect(
            center=self.surface.get_rect().center
        )
        self.surface.blit(self.content_text_surf, subtitlerect)


class TextScreen(State):
    """
    Represents a screen with text content.

    Attributes:
    -----------
    text_box: The UI text box for displaying the text content.
    """

    def __init__(self, surface: pg.Surface, screen_text: str, next_state_index: int):
        """
        Args:
        -----
        surface: The surface on which the state will be
        rendered.

        screen_text: The text content to be displayed on the screen.

        state_index: The index of the current active state.
        """
        super().__init__(surface, surface.get_size(), next_state_index)
        self.text_box = pgui.elements.UITextBox(
            screen_text, self.surface.get_rect(), self.manager
        )

    def update(self, events: list[pg.Event], time_delta: float) -> Union[int, None]:
        """
        Update the text screen state.

        Args:
        -----
        events: The list of pygame events.

        time_delta: The time elapsed since the last update.

        Returns:
        -------
        int: The index of the next state to transition to, or None if no
        transition is needed.
        """
        for event in events:
            if event.type == pg.KEYDOWN and event.key != pg.K_F11:
                return self.next_state_index
        super().update(events, time_delta)
        return None


def tint(surface: pg.Surface, color: pg.Color) -> pg.Surface:
    """create a tinted surface from the given color"""
    new_surface = surface.copy()
    new_surface.fill(color, special_flags=pg.BLEND_RGB_ADD)
    return new_surface


def get_asset_path(*paths: str):
    """Gets the path for an asset"""
    file_path = files("darwinio")
    file_path = file_path.joinpath("assets")
    for path in paths:
        file_path = file_path.joinpath(path)
    return as_file(file_path)
