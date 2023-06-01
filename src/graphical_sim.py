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
import constants


class State:
    def __init__(
        self, surf: pg.Surface, manager_size: tuple[int, int]
    ) -> None:
        self.manager = pgui.UIManager(manager_size)
        self.surface = surf

    def render(self) -> None:
        self.manager.draw_ui(self.surface)

    def update(self, events: list[pg.Event], time_delta: float):
        for event in events:
            self.manager.process_events(event)
        self.manager.update(time_delta)
        return None


class MainScreen(State):
    def __init__(self, surf: pg.Surface) -> None:
        size = height, width = surf.get_size()
        super().__init__(surf, surf.get_size())
        gui_rect = pg.Rect(-height, -width // 2, height, width // 2)
        self.game_view = pg.Surface((500, 500))
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

    def render(self) -> None:
        self.manager.draw_ui(self.surface)


class TitleScreen(State):
    def __init__(self, surf: pg.Surface, text: str) -> None:
        self.font = pg.font.SysFont("monospace", 25)
        self.title_surf = self.font.render(text, True, "white")
        self.surface = surf

    def render(self) -> None:
        self.title_surf = pg.transform.scale(
            self.title_surf,
            (self.surface.get_width(), self.title_surf.get_height()),
        )
        self.rect = self.title_surf.get_rect(
            center=self.surface.get_rect().center
        )
        self.surface.blit(self.title_surf, self.rect)

    def update(self, events: list[pg.Event], time_delta: float):
        for event in events:
            if event.type == pg.KEYDOWN:
                return 1
        self.rect = self.title_surf.get_rect(
            center=self.surface.get_rect().center
        )
        return None


class TextScreen(State):
    def __init__(self, surf: pg.Surface, text: str) -> None:
        super().__init__(surf, surf.get_size())
        self.text_box = pgui.elements.UITextBox(
            text, self.surface.get_rect(), self.manager
        )

    def update(self, events: list[pg.Event], time_delta: float):
        for event in events:
            if event.type == pg.KEYDOWN:
                return 2
        super().update(events, time_delta)


class StateMachine:
    def __init__(self, states: list[State]):
        self.states: list[State] = states
        self.state_index: int = 0

    def run_state(self, events: list[pg.Event], time_delta: float):
        state = self.states[self.state_index]
        new_state = state.update(events, time_delta)
        state.render()
        self.state_index = (
            new_state if new_state or new_state == 0 else self.state_index
        )


def main():
    pg.init()
    screen = pg.display.set_mode((1000, 750), pg.SCALED | pg.RESIZABLE)
    pg.display.set_caption("darwinio")
    clock = pg.time.Clock()
    title = TitleScreen(screen, constants.title_ascii_art)
    license_notice = TextScreen(screen, constants.license_notice)
    main_game = MainScreen(screen)
    statemachine = StateMachine([title, license_notice, main_game])

    while True:
        time_delta = clock.tick(60) / 1000.0
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
        clock.tick(60)


if __name__ == "__main__":
    main()
