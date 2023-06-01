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


class World(dist.World):
    def render(self, surface: pg.Surface):
        organisms = self.organism_distribution
        for y, row in enumerate(organisms):
            for x, organism in enumerate(row):
                if organism is not None:
                    pg.draw.rect(
                        surface, "white", pg.Rect(x * 10, y * 10, 10, 10)
                    )
                else:
                    pg.draw.rect(
                        surface, "black", pg.Rect(x * 10, y * 10, 10, 10)
                    )
        surface = pg.transform.scale(surface, surface.get_size())


class State:
    """
    Represents a game state.

    Attributes:
    -----------
    manager (pygame_gui.UIManager): The UI manager for the state.
    surface (pygame.Surface): The surface on which the state is rendered.
    """

    def __init__(self, surf: pg.Surface, manager_size: tuple[int, int]):
        """
        Args:
        ------
        surface (pygame.Surface): The surface on which the state will be rendered.
        initial_manager_size (tuple[int, int]): The initial size of the UI manager.
        """
        self.manager = pgui.UIManager(manager_size)
        self.surface: pg.Surface = surf

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


class MainScreen(State):
    """
    Represents the main screen state of the game.


    Attributes:
    -----------
    game_view (pygame.Surface): The surface for the game view.
    container (pygame_gui.core.UIContainer): The UI container for the main screen state.
    button (pygame_gui.elements.UIButton): The UI button for starting the game.
    """

    def __init__(self, surface: pg.Surface, world: World):
        """
        Args:
        -----
        surface (pygame.Surface): The surface on which the state will be rendered.
        """

        surface_size = height, width = surface.get_size()
        super().__init__(surface, surface_size)

        # User Interface
        gui_rect = pg.Rect(-height, -width // 2, height, width // 2)
        self.container = pgui.core.UIContainer(
            gui_rect,
            self.manager,
            anchors={"right": "right", "bottom": "bottom"},
        )
        self.button = pgui.elements.UIButton(
            pg.Rect(0, 0, -1, -1),
            "start",
            self.manager,
            self.container,
            anchors={"center": "center"},
        )

        # Simulation Interface
        self.running = False
        self.world = world
        self.sim_rect = pg.Rect(0, 0, height, width // 2)
        self.sim_surface = pg.surface.Surface((height, width // 2))

    def render(self) -> None:
        """Render the main screen state."""
        self.world.render(self.sim_surface)
        self.surface.blit(self.sim_surface, self.sim_rect)
        self.manager.draw_ui(self.surface)

    def update(
        self, events: list[pg.Event], time_delta: float
    ) -> Union[int, None]:
        for event in events:
            if event.type == pgui.UI_BUTTON_PRESSED:
                if event.ui_element == self.button:
                    self.running = not self.running
                    print(self.running)
            self.manager.process_events(event)
        if pg.time.get_ticks() % 1000 == 0 and self.running:
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
        int: The index of the next state to transition to, or None if no transition is needed.
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
    clock = pg.time.Clock()

    world = World((100, 100))

    # Create the states
    title = TitleScreen(screen, constants.title_ascii_art)
    license_notice = TextScreen(screen, constants.license_notice)
    main_game = MainScreen(screen, world)

    # Create the state machine
    statemachine = StateMachine([title, license_notice, main_game])

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
