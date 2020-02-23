import pygame
import sys
from pygame.locals import *
import constants
import game_objects


class Settings:

    def __init__(self, display):
        self.DISPLAY = display
        self.state = 1

    def run(self):
        # this is the main menu
        click = False

        while True:

            self.DISPLAY.fill(constants.BACKGROUND)

            mx, my = pygame.mouse.get_pos()

            main_buttons = ['Main', 'Test 1', 'Test 2', 'Test 3', 'Exit']
            second_buttons = ['Main', 'Test 1', 'Test 2', 'Test 3', 'Exit']
            button_set_list = [main_buttons, second_buttons]
            button_set = self.draw_button_set(button_set_list[0])

            if self.state == 1:
                if button_set[0].collidepoint(mx, my):
                    if click and self.state == 1:
                        return 'aoc_day10.txt'
                if button_set[1].collidepoint(mx, my):
                    if click and self.state == 1:
                        return 'aoc_day10_test1.txt'
                if button_set[2].collidepoint(mx, my):
                    if click and self.state == 1:
                        return 'aoc_day10_test2.txt'
                if button_set[3].collidepoint(mx, my):
                    if click and self.state == 1:
                        return 'aoc_day10_test3.txt'
                if button_set[4].collidepoint(mx, my):
                    if click and self.state == 1:
                        return 'Main Menu'

            if self.state == 2 or self.state == 3:
                if button_set[0].collidepoint(mx, my):
                    if click:
                        print('I am clicked')

            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button:
                        click = True
            pygame.display.update()

    def draw_button_set(self, button_name_list):

        total_buttons = []
        for num, buttons in enumerate(button_name_list):
            total_buttons.append(len(button_name_list))

        button_list = []

        surface_width = constants.BUTTON_WIDTH
        surface_height = (constants.BUTTON_HEIGHT + constants.BUTTON_OFFSET) * total_buttons[0]

        self.button_surface = pygame.Surface((surface_width, surface_height))

        for num, buttons in enumerate(button_name_list):
            button_list.append(self.draw_button(num, buttons))

        self.DISPLAY.blit(self.button_surface, (100, 100, 100, 100))

        return button_list

    def draw_button(self, button_num, text):

        button_margin = 10

        width_offset = 0
        height_offset = 100

        button = pygame.Rect(width_offset,
                             height_offset + (constants.BUTTON_HEIGHT + button_margin) * button_num,
                             constants.BUTTON_WIDTH,
                             constants.BUTTON_HEIGHT)

        menu_button_one = game_objects.MainMenuButton(button)
        menu_button_one.draw_button(self.button_surface, text)

        return button
