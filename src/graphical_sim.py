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

from typing import Union
import pygame as pg
import pygame_gui as pgui
import constants
import distribution as dist
import graphical_components as gcomp


class World(dist.World):
    """
    Renders the organisms on the given surface using the provided image.

    Args:
    -----
    surface (pg.Surface): The surface on which the organisms will be rendered.
    image (pg.Surface): The image representing an organism.
    """

    def render(self, surface: pg.Surface, image: pg.Surface):
        organisms = self.organism_distribution
        for y, row in enumerate(organisms):
            for x, organism in enumerate(row):
                if organism is not None:
                    surface.blit(image, (x * 64, y * 64))


class State:
    """
    Represents a game state.

    Attributes:
    -----------
    manager (pygame_gui.UIManager): The UI manager for the state.
    surface (pygame.Surface): The surface on which the state is rendered.
    """

    def __init__(self, surface: pg.Surface, manager_size: tuple[int, int]):
        """
        Args:
        ------
        surface (pygame.Surface): The surface on which the state will be rendered.
        initial_manager_size (tuple[int, int]): The initial size of the UI manager.
        """
        self.manager = pgui.UIManager(manager_size)
        self.surface: pg.Surface = surface

    def render(self):
        """Render the state."""
        self.manager.draw_ui(self.surface)

    def update(
        self, events: list[pg.Event], time_delta: float
    ) -> Union[int, None]:
        """
        Update the state.

        Args:
        ------
        events (list[pygame.event.Event]): The list of pygame events.
        time_delta (float): The time elapsed since the last update.

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
    states (list[State]): The list of states in the state machine.
    state_index (int): The index of the current active state.
    """

    def __init__(self, states: list[State]):
        """
        Initialize the StateMachine object.

        Args:
        -----
        states (list[State]): The list of states in the state machine.
        """
        self.states = states
        self.state_index = 0

    def run_state(self, events: list[pg.Event], time_delta: float):
        """
        Run the current active state in the state machine.

        Args:
        -----
        events (list[pg.Event]): The list of pygame events.
        time_delta (float): The time elapsed since the last update.
        """
        state = self.states[self.state_index]
        new_state = state.update(events, time_delta)
        state.render()
        self.state_index = (
            new_state
            if new_state is not None or new_state == 0
            else self.state_index
        )


class Organism_selection(State):
    """
    Represents a organism criteria selection screen.


    Attributes:
    -----------
    surface (pg.Surface): The surface on which the screen is displayed.
    world  (World): The world object containing the organisms.
    title  (pgui.elements.UITextBox): The title textbox displayed on the screen.
    energy_slider_min  (gcomp.Slider): The slider for selecting the minimum energy range of organisms.
    energy_slider_max (gcomp.Slider): The slider for selecting the maximum energy range of organisms.
    temp_slider_min (gcomp.Slider): The slider for selecting the minimum temperature range of organisms.
    temp_slider_max (gcomp.Slider): The slider for selecting the maximum temperature range of organisms.
    done_button (pgui.elements.UIButton): The button for indicating completion of organism selection.
    skip_button (pgui.elements.UIButton): The button for skipping organism selection.
    """

    def __init__(self, surface: pg.Surface, world: World):
        surface_size = width, height = surface.get_size()
        super().__init__(surface, surface_size)
        self.world: World = world

        self.title = pgui.elements.UITextBox(
            "<b>Select the range of your random organisms</b>",
            pg.Rect((width // 2) - 350 // 2, 50, 350, 50),
            self.manager,
        )

        self.energy_slider_min = gcomp.Slider(
            "Food min:", (250, 150), 100, (1, 2000), self.manager
        )
        self.energy_slider_max = gcomp.Slider(
            "Food max:", (250, 250), 1000, (1, 2000), self.manager
        )

        self.temp_slider_min = gcomp.Slider(
            "Temp min:", (250, 350), 230, (1, 2000), self.manager
        )
        self.temp_slider_max = gcomp.Slider(
            "Temp max:", (250, 450), 400, (1, 2000), self.manager
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

    def update(
        self, events: list[pg.Event], time_delta: float
    ) -> Union[int, None]:
        """
        Updates the state based on the given events and time delta.

        Args:
        -----
        events (list[pg.Event]): A list of Pygame events.
        time_delta (float): The time difference between the current and previous frame.
        """
        for event in events:
            if event.type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == self.done_button:
                    energy_range = (
                        int(self.energy_slider_min.slider.get_current_value()),
                        int(self.energy_slider_max.slider.get_current_value()),
                    )
                    temp_range = (
                        int(self.temp_slider_min.slider.get_current_value()),
                        int(self.temp_slider_max.slider.get_current_value()),
                    )
                    self.world.organism_distribution = (
                        self.world.generate_organism_distribution(
                            energy_range=energy_range, temp_range=temp_range
                        )
                    )
                    return 3
                if event.ui_element == self.skip_button:
                    return 3
            self.manager.process_events(event)

        self.energy_slider_max.update()
        self.energy_slider_min.update()
        self.temp_slider_max.update()
        self.temp_slider_min.update()

        self.manager.update(time_delta)
        return None


class Simulation(State):
    """
    Represents the main screen state of the game.


    Attributes:
    -----------
    surface (pg.Surface): The surface on which the state will be rendered.
    world (World): The world object containing the simulation data.
    image_path (str): The path to the image used for the game view.
    game_view (pygame.Surface): The surface for the game view.
    container (pygame_gui.core.UIContainer): The UI container for the main screen state.
    button (pygame_gui.elements.UIButton): The UI button for starting the game.
    image (pygame.Surface): The scaled image loaded from the image path.
    running (bool): Indicates whether the simulation is currently running.
    world_surface (pg.Surface): The surface representing the world in the simulation.
    world_rect (pg.Rect): The rectangle representing the position and size of the world surface.
    world_scale (int): The scale factor applied to the world surface.
    scaled_world_surface (pg.Surface): The world surface after applying the scale factor.
    sim_surface (pg.Surface): The simulation surface.
    sim_rect (pg.Rect): The rectangle representing the position and size of the simulation surface.
    temp_slider (gcomp.Slider): The slider for adjusting the temperature in the simulation.
    food_slider (gcomp.Slider): The slider for adjusting the food content in the simulation.
    """

    def __init__(self, surface: pg.Surface, world: World, image_path: str):
        """
        Args:
        -----
        surface (pygame.Surface): The surface on which the state will be rendered.
        world (World): The world object containing the simulation data.
        image_path: The path of the image which will be used for the organism.
        """

        surface_size = width, height = surface.get_size()
        super().__init__(surface, surface_size)

        # Simulation Interface
        self.image = pg.transform.scale(
            pg.image.load(image_path).convert_alpha(), (64, 64)
        )
        self.running = False
        self.world = world
        world_width, world_height = world.canvas_size
        self.world_surface = pg.surface.Surface(
            (world_height * 64, world_width * 64)
        )
        self.world_rect = self.world_surface.get_rect(
            center=(width // 2, height // 2)
        )
        self.world_scale = 1

        self.scaled_world_surface = self.world_surface

        self.sim_surface = pg.surface.Surface((width, height))
        self.sim_rect = self.sim_surface.get_rect(
            center=(width // 2, height // 2)
        )

        # User Interface
        self.button = pgui.elements.UIButton(
            pg.Rect(width - 100, height - 60, 100, 60), "start", self.manager
        )
        self.temp_slider = gcomp.Slider(
            "adjust temperature",
            (width - 500, height - 60),
            50,
            (0, 500),
            self.manager,
        )
        self.food_slider = gcomp.Slider(
            "adjust the food content",
            (width - 950, height - 60),
            500,
            (0, 1200),
            self.manager,
        )

    def render(self) -> None:
        """Render the main screen state."""
        self.sim_surface.fill("black")
        self.world_surface.fill("Deepskyblue3")
        self.world.render(self.world_surface, self.image)
        self.sim_surface.blit(self.scaled_world_surface, self.world_rect)
        self.surface.blit(self.sim_surface, self.sim_rect)
        self.manager.draw_ui(self.surface)

    def update(
        self, events: list[pg.Event], time_delta: float
    ) -> Union[int, None]:
        for event in events:
            if event.type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button:
                    self.running = not self.running
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.running = not self.running

            # change the temp/food content
            if event.type == pgui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.temp_slider.slider:
                    loc = self.temp_slider.slider.get_current_value()
                    self.world.temp_distribution = (
                        self.world.generate_distribution(int(loc), 50)
                    )
                    self.temp_slider.update()
                if event.ui_element == self.food_slider.slider:
                    loc = self.food_slider.slider.get_current_value()
                    self.world.food_distribution = (
                        self.world.generate_distribution(int(loc), 100)
                    )
                    self.food_slider.update()
            self.manager.process_events(event)

        keys_pressed = pg.key.get_pressed()
        # moving
        if keys_pressed[pg.K_UP] or keys_pressed[pg.K_k]:
            self.world_rect.centery += 5
        if keys_pressed[pg.K_DOWN] or keys_pressed[pg.K_j]:
            self.world_rect.centery -= 5
        if keys_pressed[pg.K_RIGHT] or keys_pressed[pg.K_l]:
            self.world_rect.centerx -= 5
        if keys_pressed[pg.K_LEFT] or keys_pressed[pg.K_h]:
            self.world_rect.centerx += 5
        # zooming
        if keys_pressed[pg.K_EQUALS] and self.world_scale < 1.5:
            self.world_scale += 0.05
            self.scaled_world_surface = pg.transform.scale_by(
                self.world_surface, self.world_scale
            )
            self.world_rect = self.scaled_world_surface.get_rect(
                center=self.world_rect.center
            )

        if keys_pressed[pg.K_MINUS] and self.world_scale > 0.2:
            self.world_scale -= 0.05
            self.scaled_world_surface = pg.transform.scale_by(
                self.world_surface, self.world_scale
            )
            self.world_rect = self.scaled_world_surface.get_rect(
                center=self.world_rect.center
            )

        if self.running:
            self.button.set_text("running")
        else:
            self.button.set_text("start")

        # run every 500 milliseconds
        if pg.time.get_ticks() % 500 == 0 and self.running:
            self.button.set_text("wait")
            self.world.update_state()

        self.manager.update(time_delta)
        return None


class TitleScreen(State):
    """
    Represents the title screen state of the game.

    Args:
    -----
    surface (pygame.Surface): The surface on which the state will be rendered.
    title_text (str): The text to be displayed as the title.

    Attributes:
    -----------
    font (pygame.font.Font): The font used for rendering the title.
    title_surf (pygame.Surface): The rendered title surface.
    surface (pygame.Surface): The surface on which the state is rendered.
    """

    def __init__(self, surface: pg.Surface, title_text: str) -> None:
        """
        Args:
        -----
        surface (pygame.Surface): The surface on which the state will be rendered.
        title_text (str): The text to be displayed as the title.
        """
        self.font = pg.font.SysFont("monospace", 25)
        self.title_surf = self.font.render(title_text, True, "white")
        self.surface = surface

    def render(self) -> None:
        """Render the title screen state."""
        self.title_surf = pg.transform.scale(
            self.title_surf,
            (self.surface.get_width(), self.title_surf.get_height()),
        )
        self.rect = self.title_surf.get_rect(
            center=self.surface.get_rect().center
        )
        self.surface.blit(self.title_surf, self.rect)

    def update(
        self, events: list[pg.Event], time_delta: float
    ) -> Union[int, None]:
        """
        Update the title screen state.

        Args:
        -----
        events (list[pygame.event.Event]): The list of pygame events.
        time_delta (float): The time elapsed since the last update.

        Returns:
        -------
        int: The index of the next state to transition to, or None if no
        transition is needed.
        """
        for event in events:
            if event.type == pg.KEYDOWN:
                return 1
        self.rect = self.title_surf.get_rect(
            center=self.surface.get_rect().center
        )
        return None


class TextScreen(State):
    """
    Represents a screen with text content.

    Attributes:
    -----------
    text_box (pygame_gui.elements.UITextBox): The UI text box for displaying the text content.
    """

    def __init__(self, surface: pg.Surface, screen_text: str):
        """
        Args:
        -----
        surface (pygame.Surface): The surface on which the state will be rendered.
        screen_text (str): The text content to be displayed on the screen.
        """
        super().__init__(surface, surface.get_size())
        self.text_box = pgui.elements.UITextBox(
            screen_text, self.surface.get_rect(), self.manager
        )

    def update(
        self, events: list[pg.Event], time_delta: float
    ) -> Union[int, None]:
        """
        Update the text screen state.

        Args:
        -----
        events (list[pygame.event.Event]): The list of pygame events.
        time_delta (float): The time elapsed since the last update.

        Returns:
        -------
        int: The index of the next state to transition to, or None if no transition is needed.
        """
        for event in events:
            if event.type == pg.KEYDOWN:
                return 2
        super().update(events, time_delta)


def main(resolution: tuple[int, int], fps: int):
    """
    The main function that runs the game.

    Args:
    -----
    resolution (tuple[int, int]): The resolution of the game screen.
    fps (int): The desired frame rate of the game.
    """

    # Initialize Pygame
    pg.init()
    screen = pg.display.set_mode(resolution, pg.SCALED | pg.RESIZABLE)
    pg.display.set_caption("darwinio")
    pg.display.set_icon(pg.image.load("../art/eubacteria_BGA.png"))
    clock = pg.time.Clock()

    world = World((100, 100))

    # Create the states
    title = TitleScreen(screen, constants.TITLE_ACSII_ART)
    license_notice = TextScreen(screen, constants.LICENSE_NOTICE)
    world_build = Organism_selection(screen, world)
    main_game = Simulation(
        screen, world, "../art/archaebacteria_halophile.png"
    )

    # Create the state machine
    statemachine = StateMachine(
        [title, license_notice, world_build, main_game]
    )

    while True:
        time_delta = clock.tick(fps) / 1000.0

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            if event.type == pg.KEYUP:
                if event.key == pg.K_F11:
                    pg.display.toggle_fullscreen()

        screen.fill("black")
        statemachine.run_state(events, time_delta)
        pg.display.flip()


if __name__ == "__main__":
    main((1000, 750), 60)
