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


class State:
    def __init__(
        self, surf: pg.Surface, manager_size: tuple[int, int]
    ) -> None:
        self.manager = pgui.UIManager(manager_size)
        self.screen = surf

    def render(self) -> None:
        self.manager.draw_ui(self.screen)

    def update(self, events: list[pg.Event], time_delta: float):
        for event in events:
            self.manager.process_events(event)
        self.manager.update(time_delta)


class TitleScreen(State):
    def __init__(self, surf: pg.Surface, text: str) -> None:
        font = pg.font.SysFont("monospace", 25)
        self.title_surf = font.render(text, True, "white")
        self.screen = surf

    def render(self) -> None:
        self.title_surf = pg.transform.scale(
            self.title_surf,
            (self.screen.get_width(), self.title_surf.get_height()),
        )
        self.rect = self.title_surf.get_rect(
            center=self.screen.get_rect().center
        )
        self.screen.blit(self.title_surf, self.rect)

    def fade(self):
        current_alpha = self.title_surf.get_alpha()
        self.title_surf.set_alpha(0)

    def update(self, events: list[pg.Event], time_delta: float):
        for event in events:
            if event.type == pg.KEYDOWN:
                self.fade()

        rect = self.title_surf.get_rect(center=self.screen.get_rect().center)


class GameScreen(State):
    pass


def main():
    title_screen = """
 ______   _______  _______          _________ _       _________ _______ 
(  __  \ (  ___  )(  ____ )|\     /|\__   __/( (    /|\__   __/(  ___  )
| (  \  )| (   ) || (    )|| )   ( |   ) (   |  \  ( |   ) (   | (   ) |
| |   ) || (___) || (____)|| | _ | |   | |   |   \ | |   | |   | |   | |
| |   | ||  ___  ||     __)| |( )| |   | |   | (\ \) |   | |   | |   | |
| |   ) || (   ) || (\ (   | || || |   | |   | | \   |   | |   | |   | |
| (__/  )| )   ( || ) \ \__| () () |___) (___| )  \  |___) (___| (___) |
(______/ |/     \||/   \__/(_______)\_______/|/    )_)\_______/(_______)
    """
    pg.init()
    screen = pg.display.set_mode((600, 500), pg.SCALED | pg.RESIZABLE)
    pg.display.set_caption("darwinio")
    clock = pg.time.Clock()
    title = TitleScreen(screen, title_screen)

    while True:
        time_delta = clock.tick(60) / 1000.0
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
        title.update(events, time_delta)
        screen.fill("black")
        title.render()
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
