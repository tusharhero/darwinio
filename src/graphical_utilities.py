import pygame as pg


class Button:
    def __init__(
        self,
        text: str,
        size: tuple[int, int],
        position: tuple[int, int],
        max_elevation: int = 6,
        font=pg.Font(None, 30),
    ) -> None:
        # core attributes
        self.max_elevation: int = max_elevation
        self.elevation: int = max_elevation
        self.position: tuple[int, int] = position

        # top rectangle
        self.top_rect = pg.Rect(position, size)
        self.top_color_not_hover = "#475F77"
        self.top_color_hover = "#D74B4B"
        self.top_color = self.top_color_not_hover

        # bottom rectangle
        self.bottom_rect = pg.Rect(position, (size[0], max_elevation))
        self.bottom_color = "#35485E"

        # text
        self.font: pg.Font = font
        self.text_color = "#FFFFFF"
        self.text_surface = self.font.render(text, False, self.text_color)
        self.text_rect = self.text_surface.get_rect(
            center=self.top_rect.center
        )

    def draw(self, screen: pg.Surface):
        self.top_rect.x = self.position[0] - self.elevation
        self.top_rect.y = self.position[1] - self.elevation

        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.elevation
        self.bottom_rect.width = self.top_rect.width + self.elevation

        pg.draw.rect(screen, self.bottom_color, self.bottom_rect)
        pg.draw.rect(screen, self.top_color, self.top_rect)
        screen.blit(self.text_surface, self.text_rect)

    def check_click(self, events: list[pg.event.Event]) -> bool:
        mouse_pos: tuple[int, int] = pg.mouse.get_pos()
        pressed = False
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.top_color_hover
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.elevation = 0
                    pressed = True
                else:
                    self.elevation = self.max_elevation
        else:
            self.top_color = self.top_color_not_hover
        return pressed
