import math
import constants
import game_objects


def readfile(filename):
    read_file = open(filename)
    file_input = []

    # read each line of the text file
    for line in read_file:
        file_input.append(list(line.strip()))

    return file_input


def get_asteroid_list(asteroid_map):
    asteroid_list = []

    for i, j in enumerate(asteroid_map):
        for k, l in enumerate(j):

            if l == '#':
                asteroid_list.append([k, i])

    return asteroid_list


def calculate_angle(x, y):
    """
      tangent = opposite/adjacent

          0 <= angle < 90: quadrant I
          90 <= angle < 180: quadrant II
          180 <= angle < 270: quadrant III
          270 <= angle < 360: quadrant IV

          if ydiff > 0 and xdiff == 0:
              angle = 90 degrees, so quadrant is II
          if ydiff < 0 and xdiff == 0:
              angle = 270 degrees, so quadrant is IV
          if ydiff == 0 and xdiff > 0:
              angle = 0 degrees, so quadrant is I
         if ydiff == 0 and xdiff < 0:
              angle = 180 degrees, so quadrant is III
    """

    x_abs = abs(x)
    y_abs = abs(y)
    angle = 0

    # edge checks
    if y > 0 and x == 0:
        angle = (1 / 2) * math.pi
    elif y < 0 and x == 0:
        angle = (3 / 2) * math.pi
    elif y == 0 and x > 0:
        angle = 0
    elif y == 0 and x < 0:
        angle = math.pi
    # calculate actual angle
    elif y > 0 and x > 0:
        angle = math.atan(y_abs / x_abs)
    elif y > 0 and x < 0:
        angle = math.pi - math.atan(y_abs / x_abs)
    elif y < 0 and x < 0:
        angle = math.pi + math.atan(y_abs / x_abs)
    elif y < 0 and x > 0:
        angle = 2 * math.pi - math.atan(y_abs / x_abs)
    else:
        print(y, x)
        print('Cannot calculate angle!')

    return angle


def radians_to_degrees(angle):

    return angle * (180/math.pi)


def build_asteroid_dictionary(asteroid_list, asteroid):
    """
      This function builds a dictionary of asteroids around
      the asteroid input. Each key in the dictionary is the
      angle between the target asteroid and the asteroid input.
      Each value in the dictionary is a list of asteroids at that angle.

      If the angle (key) already exists, then you are adding the
      target asteroid to the asteroid list associated with the key.

      In this way, each key gives the number of asteroids at that angle.
    """

    asteroid_dictionary = {}

    for target_asteroid in asteroid_list:

        x_diff = target_asteroid[0] - asteroid[0]
        y_diff = target_asteroid[1] - asteroid[1]

        if x_diff == 0 and y_diff == 0:
            # if it's the same point, don't do any calculations
            continue
        else:
            angle = calculate_angle(x_diff, y_diff)

        if angle in asteroid_dictionary:
            asteroid_dictionary[angle].append(target_asteroid)
        else:
            asteroid_dictionary[angle] = [target_asteroid]

    return asteroid_dictionary


def find_monitoring_station(asteroid_list):
    """
      This function finds the best monitoring station so that it can
      destroy the most number of asteroids in the fewest possible turns.
    """

    maximum = 0
    max_dictionary = {}
    max_asteroid = []

    for asteroid in asteroid_list:

        asteroid_dictionary = build_asteroid_dictionary(asteroid_list, asteroid)

        if len(asteroid_dictionary) > maximum:
            maximum = len(asteroid_dictionary)
            max_dictionary = asteroid_dictionary
            max_asteroid = asteroid

    return max_dictionary, max_asteroid


def get_sorted_keys(dictionary):
    """
    This function sorts the keys of a dictionary (input) from smallest to largest, and returns a list of the keys
    in sorted order. You can then run through the dictionary in sorted order. In this case the keys are the angles
    between the monitoring station and each target asteroid list.

    :param dictionary: A generic dictionary. In this case, a dictionary of angles (key) to a list of asteroid
    coordinates
    :return sorted_list: A list of keys sorted from smallest to largest
    """
    sorted_list = []

    for key in dictionary:
        index = 0
        done = False

        while index < len(sorted_list):
            entry = sorted_list[index]
            if key < entry:
                sorted_list.insert(index, key)
                done = True
                break
            index += 1

        if not done:
            sorted_list.append(key)

    return sorted_list


def find_index(keys_list, value):
    """
    This function returns the first index in which the element is greater than the value parameter in the keys_list.
    The keys_list is a list sorted from smallest to largest (See: get_sorted_keys function).

    For example, if you had a keys_list: [1, 2, 4, 5] and a value of 3, this function would return the index of 2,
    since index 2 is the first element (4) that is larger than 3.

    :param keys_list: a list of sorted values from smallest to largest.
    :param value: the value to use to compare against each entry in the keys_list
    :return index: the index of the keys_list where value of that index is greater than the value parameter. If there
    are no elements greater than the value parameter, the index returned is 0.
    """
    # find where to start
    for index, entry in enumerate(keys_list):

        if value <= entry:
            return index

    return 0


def get_distance(x, y):
    return math.sqrt(x ** 2 + y ** 2)


def calculate_min_distance(origin, target_list):
    """
    This function calculates the minimum distance between the origin (x and y coordinates) and the target_list (list
    of coordinates). This is used to find the closest asteroid to the monitoring station for a given set of asteroids
    at a given angle

    :param origin: 1D list, where x coordinate is list[0] and y coordinate is list[1]
    :param target_list: 2D list, where each entry is a set of coordinates.
    :return: coordinates (in list form) of the closest target (asteroid) to the origin
    """
    min_distance = 0
    min_target = []

    for index, entry in enumerate(target_list):
        x_diff = entry[0] - origin[0]
        y_diff = entry[1] - origin[1]
        distance = get_distance(x_diff, y_diff)

        if distance < min_distance or index == 0:
            min_distance = distance
            min_target = entry

    return min_target


def draw_asteroid_grid(display, asteroid_surface, asteroid_grid, images, angle):

    num_cols = len(asteroid_grid[0])
    num_rows = len(asteroid_grid)

    (asteroid_surface_width, asteroid_surface_height) = asteroid_surface.get_size()

    tile_width = asteroid_surface_width // num_cols
    tile_height = asteroid_surface_height // num_rows

    tile_offset_width = constants.SCREEN_WIDTH - asteroid_surface_width
    tile_offset_height = constants.SCREEN_HEIGHT - asteroid_surface_height

    asteroid_radius = 5
    asteroid_thickness = 1

    station_width = asteroid_radius * 2
    station_height = station_width
    station_thickness = 1
    image_monitoring_station = images['monitoring_station'][0]
    image_asteroid = images['asteroids'][0]

    for i, rows in enumerate(asteroid_grid):
        for j, columns in enumerate(rows):

            if columns == '#':
                game_objects.Asteroid(asteroid_surface, image_asteroid, j * tile_width + tile_width // 2,
                                      i * tile_height + tile_height // 2,
                                      asteroid_radius, asteroid_thickness).draw()
            if columns == 'X':
                game_objects.Station(asteroid_surface, image_monitoring_station, j * tile_width + tile_width // 2,
                                     i * tile_height + tile_height // 2, angle, station_thickness).draw()
            if columns == '*':
                game_objects.Asteroid(asteroid_surface, image_asteroid, j * tile_width + tile_width // 2,
                                      i * tile_height + tile_height // 2,
                                      asteroid_radius + 10).draw()

    display.blit(asteroid_surface, (tile_offset_width, tile_offset_height))
