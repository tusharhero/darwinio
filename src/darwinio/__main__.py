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
import pygame as pg
import darwinio.graphical_sim as gsim
import darwinio.constants as constants


def main(resolution: tuple[int, int], fps: int, world_size: tuple[int, int]):
    """
    The main function that runs the game.

    Args:
    -----
    resolution (tuple[int, int]): The resolution of the game screen.

    fps (int): The desired frame rate of the game.

    world_size (tuple[int, int]): The size of the world for simulation.
    """

    # Initialize Pygame
    pg.init()
    screen = pg.display.set_mode(resolution, pg.SCALED | pg.RESIZABLE)
    pg.display.set_caption("darwinio")
    with gsim.get_asset_path("art", "eubacteria_BGA.png") as path:
        pg.display.set_icon(pg.image.load(path))
    clock = pg.time.Clock()

    # music
    music_playing = True
    with gsim.get_asset_path("audio", "Darwinio.mp3") as path:
        pg.init()
        pg.mixer.music.load(path)
        pg.mixer.music.set_volume(1)
        pg.mixer.music.play()

    world = gsim.World(world_size)

    # Create the states
    title = gsim.TitleScreen(screen, constants.TITLE_ASCII_ART)
    license_notice = gsim.TextScreen(screen, constants.LICENSE_NOTICE, 2)
    world_build = gsim.Organism_selection(screen, world)
    help_screen = gsim.TextScreen(screen, constants.HELP, 4)
    with gsim.get_asset_path("art", "archaebacteria_halophile.png") as path:
        main_game = gsim.Simulation(screen, world, path)

    # Create the state machine
    statemachine = gsim.StateMachine(
        [title, license_notice, world_build, main_game, help_screen]
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
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    raise SystemExit
                if event.key == pg.K_m:
                    if music_playing:
                        pg.mixer.music.pause()
                    else:
                        pg.mixer.music.unpause()
                        music_playing = not music_playing
                if event.mod & pg.KMOD_LSHIFT and event.key == pg.K_h:
                    prev_index: int = statemachine.state_index
                    statemachine.state_index = 4
                    help_screen.next_state_index = prev_index

        screen.fill("#423E4A")
        statemachine.run_state(events, time_delta)
        pg.display.flip()


if __name__ == "__main__":
    main((1000, 750), 60, (50, 50))
