import pygame
import constants


class Asteroid:

    def __init__(self, surface, image, center_x, center_y, asteroid_radius=10, asteroid_thickness=0,
                 asteroid_color=constants.GREEN):
        self.surface = surface
        self.center_x = center_x
        self.center_y = center_y
        self.asteroid_radius = asteroid_radius
        self.asteroid_thickness = asteroid_thickness
        self.asteroid_color = asteroid_color
        self.image = image

    def draw(self):
        asteroid_rect = self.image.get_rect(center=(self.center_x, self.center_y))
        self.surface.blit(self.image, asteroid_rect)
        #pygame.draw.circle(self.surface, self.asteroid_color, (self.center_x, self.center_y), self.asteroid_radius,
                           #self.asteroid_thickness)

    def set_color(self, asteroid_color):
        self.asteroid_color = asteroid_color

    def set_radius(self, asteroid_radius):
        self.asteroid_radius = asteroid_radius

    def set_thickness(self, asteroid_thickness):
        self.asteroid_thickness = asteroid_thickness


class Station:

    def __init__(self, surface, image, center_x, center_y, angle, station_thickness=1,
                 station_color=constants.GREEN):
        self.surface = surface
        self.image = pygame.transform.rotate(image, angle)
        self.center_x = center_x
        self.center_y = center_y
        self.station_thickness = station_thickness
        self.station_color = station_color

    def draw(self):
        station_rect = self.image.get_rect(center=(self.center_x, self.center_y))
        self.surface.blit(self.image, station_rect)

    def set_color(self, station_color):
        self.station_color = station_color

    def set_thickness(self, station_thickness):
        self.station_thickness = station_thickness


class MainMenuButton:

    def __init__(self, rect):
        self.rect = rect
        self.left = rect.left
        self.top = rect.top
        self.width = rect.width
        self.height = rect.height

    def draw_button(self, display, text):
        # render the font
        menu_font = pygame.font.SysFont('couriernew', 20)
        font_surface = menu_font.render(text, True, constants.GREEN)

        # center the font in the rectangle
        font_width, font_height = menu_font.size(text)
        margin_width = (self.width - font_width) // 2
        margin_height = (self.height - font_height) // 2
        font_rect = pygame.Rect(self.left + margin_width, self.top + margin_height, font_width, font_height)

        # blit the font
        display.blit(font_surface, font_rect)

        # draw the rectangle
        pygame.draw.rect(display, constants.GREEN, self.rect, 1)
