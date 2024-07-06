import numpy as np
import matplotlib.pyplot as plt
import pygame
from PIL import Image
import heapq
import csv


def create_matrix_from_image(image_path, threshold=0.3):
    """Function that given a black and white image, transforms it into a binary matrix.

    Args:
        image_path (string): the path to the image
        threshold (float): if a cell is more than threshold % black then it becomes entirely black

    Returns:
        np.ndarray: The representation of the map as a matrix of 1s and 0s
    """
    try:
        img = Image.open(image_path).convert('L')
    except IOError:
        print("Error: Unable to open image file.")
        return None

    img = np.array(img)
    matrix = np.zeros_like(img, dtype=int)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j] < 128:
                matrix[i, j] = 1  # Walkable path
            else:
                matrix[i, j] = 0  # Obstacle

    return matrix


def heuristic(a, b):
    """Helper for the A-Star algorithm

    Args:
        a (tuple[int]): first point position
        b (tuple[int]): second point position

    Returns:
        int: Manhattan distance between the points
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(matrix, start, goal):
    """Performs the A* algorithm to find the shortest path from start to goal in a grid matrix.

    Args:
        matrix (np.ndarray): A 2D grid representing the map where 0 is an obstacle and 1 is a walkable path.
        start (tuple): The starting coordinate (row, column) in the grid.
        goal (tuple): The goal coordinate (row, column) in the grid.

    Returns:
        list: A list of coordinates representing the path from start to goal. If no path is found, returns False.
    """
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.reverse()
            return data

        close_set.add(current)
        for _, (i, j) in enumerate(neighbors):
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + 1
            if 0 <= neighbor[0] < matrix.shape[0]:
                if 0 <= neighbor[1] < matrix.shape[1]:
                    if matrix[neighbor[0]][neighbor[1]] == 0:  # Obstacle
                        continue
                else:
                    continue
            else:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False


def get_direction(from_node, to_node):
    """Determines the direction of movement from one node to another in a grid.
    Args:
        from_node (tuple): The starting coordinate (row, column).
        to_node (tuple): The destination coordinate (row, column).

    Returns:
        str: The direction of movement as a string. Possible values are 'right', 'left', 'down', 'up', or 'straight'.
    """
    if from_node[0] == to_node[0]:
        if from_node[1] < to_node[1]:
            return 'right'
        else:
            return 'left'
    elif from_node[1] == to_node[1]:
        if from_node[0] < to_node[0]:
            return 'down'
        else:
            return 'up'
    return 'straight'


def save_path_with_direction_changes(path, filename="gps.csv"):
    """Saves the coordinates where there is a change in direction to a CSV file.

    Args:
        path (list): The list of coordinates representing the path.
        filename (str): The name of the output CSV file.
    """
    directions = []
    for i in range(len(path) - 1):
        direction = get_direction(path[i], path[i + 1])
        if i == 0 or direction != directions[-1][1]:
            directions.append((i, path[i][0], path[i][1], direction))

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["X", "Y"])
        for _, x, y, _ in directions:
            writer.writerow([y, x])


def save_followed_directions(path, filename="offline.csv"):
    """Saves a count and the direction of the same directions to a CSV file.

    Args:
        path (list): The list of coordinates representing the path.
        filename (str): The name of the output CSV file.
    """
    directions = []
    current_direction = None
    meter_count = 0

    for i in range(len(path) - 1):
        direction = get_direction(path[i], path[i + 1])
        if direction == current_direction:
            meter_count += 1
        else:
            if current_direction is not None:
                directions.append((meter_count, current_direction))
            current_direction = direction
            meter_count = 1

    if current_direction is not None:
        directions.append((meter_count, current_direction))

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["METER", "DIRECTION"])
        for meter, direction in directions:
            writer.writerow([meter, direction])


# Load and create matrix
image_path = 'files/map_avidan.png'
map_img = pygame.image.load(image_path)
matrix = create_matrix_from_image(image_path)

if matrix is not None:
    # Display the matrix and allow user to select two points
    figure, axes = plt.subplots()
    axes.imshow(matrix, cmap='gray')

    points = []

    def onclick(event):
        if len(points) < 2:
            ix, iy = int(event.xdata), int(event.ydata)
            points.append((iy, ix))
            axes.plot(ix, iy, 'ro')
            figure.canvas.draw()
            if len(points) == 2:
                path = a_star(matrix, points[0], points[1])
                if path:
                    # Create an RGB version of the matrix for colored path visualization
                    rgb_matrix = np.zeros((matrix.shape[0], matrix.shape[1], 3), dtype=float)
                    rgb_matrix[matrix == 1] = [1, 1, 1]  # Walkable path in white
                    rgb_matrix[matrix == 0] = [0, 0, 0]  # Obstacle in black

                    for (x, y) in path:
                        rgb_matrix[x, y] = [0, 1, 0]  # Green color for the path

                    axes.imshow(rgb_matrix)
                    figure.canvas.draw()

                    # Save directions to CSV
                    save_path_with_direction_changes(path)
                    save_followed_directions(path)
                else:
                    print("No path found")

    def zoom(event):
        base_scale = 1.1
        cur_xlim = axes.get_xlim()
        cur_ylim = axes.get_ylim()
        xdata = event.xdata
        ydata = event.ydata
        if event.button == 'up':
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            scale_factor = base_scale
        else:
            scale_factor = 1
            print(event.button)
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
        axes.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        axes.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])
        axes.figure.canvas.draw()


    cid_click = figure.canvas.mpl_connect('button_press_event', onclick)
    cid_scroll = figure.canvas.mpl_connect('scroll_event', zoom)

    plt.show()
else:
    print("Failed to create matrix from the image.")
