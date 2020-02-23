import pygame
import sys
from pygame.locals import *
import utilityfunctions
import copy
import constants
import game_objects
import game_mode_two
import settings


class Game:

    def __init__(self):
        pygame.init()
        self.DISPLAY = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        pygame.display.set_caption('Asteroids')
        self.asteroid_grid = []
        self.asteroid_grid_copy = []
        self.asteroid_list = []
        self.asteroid_list_copy = []
        self.state = ''
        self.re_init('aoc_day10.txt')
        space_ship = pygame.image.load('space_ship.png')
        asteroid_one = pygame.image.load('asteroid_1.png')
        self.images = {'monitoring_station': [space_ship], 'asteroids': [asteroid_one]}

    def re_init(self, file_name):
        self.asteroid_grid = utilityfunctions.readfile(file_name)
        self.asteroid_grid_copy = copy.deepcopy(self.asteroid_grid)
        self.asteroid_list = utilityfunctions.get_asteroid_list(self.asteroid_grid)
        self.asteroid_list_copy = self.asteroid_list.copy()
        self.state = 'init'

    def run(self):
        # this is the main menu
        click = False
        value = ''

        while True:

            self.DISPLAY.fill(constants.BACKGROUND)

            self.draw_title('Advent of Code Day 10')

            self.draw_subtitle('Asteroid Exploder')

            mx, my = pygame.mouse.get_pos()

            total_buttons = 3

            button_one = self.draw_button(0, total_buttons, 'Run')
            button_two = self.draw_button(1, total_buttons, 'Settings')
            button_three = self.draw_button(2, total_buttons, 'Quit')

            if button_one.collidepoint(mx, my):
                if click:
                    value = self.run_mode_two()
            if button_two.collidepoint(mx, my):
                if click:
                    value = self.run_settings()
                    # TODO: check to see if file exists?
                    if value != 'Main Menu':
                        self.re_init(value)
            if button_three.collidepoint(mx, my):
                if click:
                    pygame.quit()
                    sys.exit()

            if value == 'restart':
                value = self.run_mode_two()

            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button:
                        click = True
            if value != 'restart':
                pygame.display.update()

    def run_mode_two(self):
        mode_two = game_mode_two.GameModeTwo(self.DISPLAY, self.asteroid_grid, self.asteroid_list, self.images)
        value = mode_two.run()
        return value

    def run_settings(self):
        settings_run = settings.Settings(self.DISPLAY)
        value = settings_run.run()
        return value

    def draw_button(self, button_num, total_buttons, text):

        button_margin = 20

        total_width = (constants.BUTTON_WIDTH + button_margin) * total_buttons

        width_offset = constants.SCREEN_WIDTH // 2 - total_width // 2
        height_offset = (constants.SCREEN_HEIGHT * 2) // 3 - constants.BUTTON_HEIGHT // 2

        button = pygame.Rect(width_offset + (constants.BUTTON_WIDTH + button_margin) * button_num,
                             height_offset,
                             constants.BUTTON_WIDTH,
                             constants.BUTTON_HEIGHT)

        menu_button_one = game_objects.MainMenuButton(button)
        menu_button_one.draw_button(self.DISPLAY, text)

        return button

    def draw_title(self, text):

        title_font = pygame.font.SysFont('couriernew', 40)
        font_surface = title_font.render(text, True, constants.GREEN)

        # center the font in the rectangle
        font_width, font_height = title_font.size(text)
        rect_left = constants.SCREEN_WIDTH // 2 - font_width // 2
        rect_top = constants.SCREEN_HEIGHT // 3 - font_height // 2

        font_rect = pygame.Rect(rect_left, rect_top, font_width, font_height)

        # blit the font
        self.DISPLAY.blit(font_surface, font_rect)

    def draw_subtitle(self, text):

        title_font = pygame.font.SysFont('couriernew', 25)
        font_surface = title_font.render(text, True, constants.GREEN)

        # center the font in the rectangle
        font_width, font_height = title_font.size(text)
        rect_left = constants.SCREEN_WIDTH // 2 - font_width // 2
        rect_top = constants.SCREEN_HEIGHT // 3 - font_height // 2 + 60

        font_rect = pygame.Rect(rect_left, rect_top, font_width, font_height)

        # blit the font
        self.DISPLAY.blit(font_surface, font_rect)


# End game class


if __name__ == "__main__":
    Game().run()
