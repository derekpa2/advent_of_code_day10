import pygame
import sys
from pygame.locals import *
import utilityfunctions
import math
import copy
import constants
import game_objects


class GameModeTwo:

    def __init__(self, display, asteroid_grid, asteroid_list, images):
        self.DISPLAY = display
        self.asteroid_surface = pygame.Surface((constants.ASTEROID_WINDOW_WIDTH, constants.ASTEROID_WINDOW_HEIGHT))
        self.asteroid_grid = copy.deepcopy(asteroid_grid)
        self.asteroid_list = copy.deepcopy(asteroid_list)
        self.images = images

        self.min_distance_asteroid = []
        self.counter = 0
        self.found_counter = 0
        self.state = 'find'
        self.prev_state = 'find'

        self.asteroid_dictionary, self.monitoring_station = utilityfunctions.find_monitoring_station(self.asteroid_list)
        self.asteroid_grid[self.monitoring_station[1]][self.monitoring_station[0]] = 'X'
        self.asteroid_list.remove(self.monitoring_station)
        self.sorted_keys = utilityfunctions.get_sorted_keys(self.asteroid_dictionary)
        self.index = utilityfunctions.find_index(self.sorted_keys, (3 / 2) * math.pi)
        self.current_angle = 0

    def run(self):
        """
        There are x states:

            - 'find' -> in this state the program is looking for an asteroid to blow up
            - 'found, exploding' -> in this state the program has found an asteroid and is blowing it up
            - 'finished' -> currently unused. but it indicates when the game is finished.

        :return: returns a string indicating whether to restart or return to the main menu.
        """

        click = False
        paused = False
        paused_string = 'Pause'

        # mode two game loop
        while True:

            self.DISPLAY.fill(constants.BACKGROUND)
            self.asteroid_surface.fill(constants.BACKGROUND)

            # If all the asteroids are removed, then the game is finished. Display paused screen
            # NOTE: currently 'finished' state doesn't do anything

            if len(self.asteroid_list) == 0:
                self.asteroid_surface.fill(constants.PAUSED_BACKGROUND)
                self.DISPLAY.blit(self.asteroid_surface, (constants.ASTEROID_WINDOW_OFFSET, 0))
                self.state = 'finished'

            if paused:
                self.asteroid_surface.fill(constants.PAUSED_BACKGROUND)
                self.DISPLAY.blit(self.asteroid_surface, (constants.ASTEROID_WINDOW_OFFSET, 0))
            else:
                if self.state == 'find':
                    self.find_state()
                elif self.state == 'found':
                    self.found_state()

            mx, my = pygame.mouse.get_pos()

            # Create the Buttons
            num_buttons = 0
            button_one = self.draw_button(num_buttons, paused_string)

            num_buttons += 1
            button_two = self.draw_button(num_buttons, 'Restart')

            num_buttons += 1
            button_three = self.draw_button(num_buttons, 'Main Menu')

            num_buttons += 1
            button_four = self.draw_button(num_buttons, 'Quit')

            if button_one.collidepoint(mx, my):
                if click:
                    if paused:
                        paused = False
                        paused_string = 'Pause'
                    else:
                        paused = True
                        paused_string = 'Play'

            if button_two.collidepoint(mx, my):
                if click:
                    return 'restart'
            if button_three.collidepoint(mx, my):
                if click:
                    return 'return to main menu'
            if button_four.collidepoint(mx, my):
                if click:
                    pygame.quit()
                    sys.exit()

            utilityfunctions.draw_asteroid_grid(self.DISPLAY, self.asteroid_surface, self.asteroid_grid, self.images,
                                                self.current_angle)

            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button:
                        click = True
            pygame.display.update()

    def find_state(self):

        self.found_counter = 0
        if self.index < len(self.sorted_keys):
            key = self.sorted_keys[self.index]
            self.index += 1
        else:
            key = self.sorted_keys[0]
            self.index = 1

        if self.asteroid_dictionary[key]:
            self.counter += 1
            self.min_distance_asteroid = utilityfunctions.calculate_min_distance(self.monitoring_station,
                                                                                 self.asteroid_dictionary[key])
            self.current_angle = 270 - utilityfunctions.radians_to_degrees(key)
            print(key, self.current_angle)
            self.asteroid_list.remove(self.min_distance_asteroid)
            self.asteroid_dictionary[key].remove(self.min_distance_asteroid)
            self.asteroid_grid[self.min_distance_asteroid[1]][self.min_distance_asteroid[0]] = '*'
            self.state = 'found'

    def found_state(self):
        if self.found_counter >= 1:
            self.asteroid_grid[self.min_distance_asteroid[1]][self.min_distance_asteroid[0]] = ' '
            self.state = 'find'
        self.found_counter += 1

    def draw_button(self, num_buttons, text_string):

        button_margin = 10

        button = pygame.Rect(constants.BUTTON_OFFSET,
                             constants.BUTTON_HEIGHT * num_buttons + button_margin * (num_buttons + 1),
                             constants.BUTTON_WIDTH,
                             constants.BUTTON_HEIGHT)
        menu_button_one = game_objects.MainMenuButton(button)
        menu_button_one.draw_button(self.DISPLAY, text_string)

        return button
