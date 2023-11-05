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

from importlib.metadata import distribution, version

import pygame as pg

import darwinio.constants as constants
import darwinio.graphical_sim as gsim
import darwinio.stats as statistics


def main(resolution: tuple[int, int], fps: int, world_size: tuple[int, int]):
    """
    The main function that runs the game.

    Args:
    -----
    resolution: The resolution of the game screen.

    fps: The desired frame rate of the game.

    world_size: The size of the world for simulation.
    """

    # Initialize Pygame
    pg.init()
    screen = pg.display.set_mode(resolution, pg.SCALED | pg.RESIZABLE)
    pg.display.set_caption(f'darwinio v{version("darwinio")}')
    with gsim.get_asset_path("art", "eubacteria_BGA.png") as path:
        pg.display.set_icon(pg.image.load(path))
    clock = pg.time.Clock()

    # music
    music_playing = True
    with gsim.get_asset_path("audio", "Darwinio.ogg") as path:
        pg.mixer.music.load(path)
    pg.mixer.music.set_volume(1)
    pg.mixer.music.play()

    world = gsim.World(world_size, initial_temp_avg=45)
    stats = statistics.StatisticsCollector(
        ["Population", "Food", "Temperature", "Reproduction Ratio"]
    )

    # Create the states
    title = gsim.TitleScreen(
        screen, constants.TITLE_ASCII_ART, f'v{version("darwinio")}', 1
    )
    disclaimer = gsim.HeadingTextScreen(screen, "DISCLAIMER", constants.DISCLAIMER, 2)
    license_notice = gsim.TextScreen(screen, constants.LICENSE_NOTICE, 3)
    organism_build = gsim.OrganismSelection(screen, world, 5)
    init_help_screen = gsim.TextScreen(screen, constants.HELP, 4)
    help_screen = gsim.TextScreen(screen, constants.HELP, 6)
    distribution_painting = gsim.DistributionPainting(screen, world, 4)

    # get images for the organisms.
    image_names: list[str] = [
        "archaebacteria_halophile.png",
        "archaebacteria_methanogen.png",
        "archaebacteria_thermoacidophile.png",
        "eubacteria_BGA.png",
        "eubacteria_mycoplasma.png",
        "eubacteroa_chemosynthetic.png",
        "fungi-ascomycetes.png",
        "fungi-basidiomycetes.png",
        "fungi-deuteromycetes.png",
        "fungi-phycomycetes.png",
        "metaphyta-algae.png",
        "metaphyta-angiospermae.png",
        "metaphyta-bryophyta.png",
        "metaphyta-gymnospermae.png",
        "metaphyta-pterdiophyta.png",
        "protista_dinoflagellate.png",
        "protista_euglena.png",
        "protista_protozoan.png",
        "protista_slimemould.png",
    ]
    images: list[pg.Surface] = []
    for file_name in image_names:
        with gsim.get_asset_path("art", file_name) as path:
            images.append(
                pg.transform.scale(pg.image.load(path).convert_alpha(), (64, 64))
            )

    main_game = gsim.Simulation(screen, world, stats, images)

    # Create the state machine
    statemachine = gsim.StateMachine(
        [
            title,
            disclaimer,
            license_notice,
            init_help_screen,
            organism_build,
            main_game,
            help_screen,
            distribution_painting,
        ]
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
                        music_playing = not music_playing
                    else:
                        pg.mixer.music.unpause()
                        music_playing = not music_playing
                if event.mod & pg.KMOD_LSHIFT and event.key == pg.K_h:
                    prev_index: int = statemachine.state_index
                    statemachine.state_index = 5
                    help_screen.next_state_index = prev_index

        screen.fill("#000000")
        statemachine.run_state(events, time_delta)
        pg.display.flip()


def cli():
    main((1000, 750), 60, (50, 50))


if __name__ == "__main__":
    cli()
