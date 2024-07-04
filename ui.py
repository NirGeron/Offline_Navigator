import time
import pygame
import csv
import read_map
from PIL import Image

# Initialize Pygame
pygame.init()

# Constants
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Load images
map_img = pygame.image.load("files/map_grayscale.png")
car_img = pygame.image.load("files/arrow.png")

# Get map dimensions and set the window size accordingly
map_width, map_height = map_img.get_size()
window = pygame.display.set_mode((map_width, map_height))
pygame.display.set_caption("Navigator Simulation")

# Scale car image
car_img = pygame.transform.scale(car_img, (30, 30))

# Font for rendering text
font = pygame.font.SysFont(None, 24)


# Function to read CSV file
def read_csv(file_path):
    points = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if there is one
        for row in reader:
            x, y, yaw = map(float, row)
            points.append((x, y, yaw))
    return points


# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def show_bubble_error(message, window):
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)
    error_width = 400
    error_height = 200
    error_x = map_width // 2
    error_y = map_height // 2

    pygame.draw.rect(window, WHITE, (error_x, error_y, error_width, error_height), border_radius=20)
    pygame.draw.rect(window, RED, (error_x, error_y, error_width, error_height), width=2, border_radius=20)

    text_surf = font.render("Error", True, RED)
    text_rect = text_surf.get_rect(center=(error_x + error_width // 2, error_y + 40))
    window.blit(text_surf, text_rect)

    message_lines = message.split("\n")
    line_y = error_y + 80
    for line in message_lines:
        text_surf = font.render(line, True, BLACK)
        text_rect = text_surf.get_rect(center=(error_x + error_width // 2, line_y))
        window.blit(text_surf, text_rect)
        line_y += 30

    ok_button = pygame.Rect(error_x + error_width // 2 - 50, error_y + error_height - 60, 100, 40)
    pygame.draw.rect(window, RED, ok_button)
    ok_text = font.render("OK", True, WHITE)
    ok_text_rect = ok_text.get_rect(center=ok_button.center)
    window.blit(ok_text, ok_text_rect)

    pygame.display.update()
    pygame.display.flip()


# Function to check if the car is on the road
def is_on_road(pos):
    x, y = int(pos[0]), int(pos[1])
    if read_map.check_road(x, y):
        return True
    return False


# Load the points from CSV
points = read_csv("files/points.csv")

# Car properties
car_pos = [points[0][0], points[0][1]]
car_yaw = points[0][2]
car_speed = 0  # Initial speed
max_speed = 1  # Maximum speed
acceleration = 0.01  # Acceleration rate
deceleration = 0.04  # Deceleration rate
yaw_speed = 5  # Speed of yaw change
range_yaw = 60

# Main loop
running = True
clock = pygame.time.Clock()
path = [(110, 0), (280, -90), (370, 0)]

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Calculate new position
    new_pos = car_pos.copy()
    if keys[pygame.K_UP]:
        new_pos[0] += car_speed * pygame.math.Vector2(1, 0).rotate(-car_yaw).x
        new_pos[1] += car_speed * pygame.math.Vector2(1, 0).rotate(-car_yaw).y
    if keys[pygame.K_DOWN]:
        new_pos[0] -= car_speed * pygame.math.Vector2(1, 0).rotate(-car_yaw).x
        new_pos[1] -= car_speed * pygame.math.Vector2(1, 0).rotate(-car_yaw).y

    # Check if the new position is on the road

    # car_pos = new_pos
    # Adjust speed
    if keys[pygame.K_UP]:
        car_speed += acceleration
        if car_speed > max_speed:
            car_speed = max_speed
    elif keys[pygame.K_DOWN]:
        car_speed -= acceleration
        if car_speed < -max_speed / 2:  # Reverse speed limit
            car_speed = -max_speed / 2
    else:
        if car_speed > 0:
            car_speed -= deceleration
            if car_speed < 0:
                car_speed = 0
        elif car_speed < 0:
            car_speed += deceleration
            if car_speed > 0:
                car_speed = 0

    # Turn the car
    if keys[pygame.K_LEFT]:
        car_yaw += yaw_speed
    if keys[pygame.K_RIGHT]:
        car_yaw -= yaw_speed

    # Clear the screen
    window.fill(WHITE)

    # Draw the map
    window.blit(map_img, (0, 0))

    if is_on_road(new_pos):
        car_pos = new_pos
    else:
        car_pos = new_pos
        road_text = "not on road"
        draw_text(road_text, font, (238, 0, 99), window, 10, 40)
    # Rotate the car image
    rotated_car = pygame.transform.rotate(car_img, car_yaw)
    rect = rotated_car.get_rect(center=(car_pos[0], car_pos[1]))

    # Draw the car
    window.blit(rotated_car, rect.topleft)

    if len(path) == 0:
        show_bubble_error("you've arrived", window)
        time.sleep(20)
    elif len(path) >= 2:
        next_turn = f"turn {path[1][1]} in {path[0][0]} meters"
    else:
        next_turn = f"keep straight and in {path[0][0]} meters you will arrive"

    if car_yaw - range_yaw <= path[0][1] <= car_yaw + range_yaw:
        path[0] = (int(path[0][0] - (0.1* car_speed)), path[0][1])
    if path[0][0] == 0:
        print(path)
        path = path[1:]
    # Draw text
    position_text = f"Position: ({car_pos[0]:.1f}, {car_pos[1]:.1f})"
    yaw_text = f"Yaw: {car_yaw:.1f}, speed: {100 * car_speed:.1f}"
    draw_text(position_text, font, (0, 0, 0), window, 10, 10)
    draw_text(yaw_text, font, (0, 0, 0), window, 10, 30)
    draw_text(next_turn, font, (0, 0, 0), window, 10, 40)

    # Update the display
    pygame.display.flip()

for i in range(1000):
    show_bubble_error("Not on road!", window)

pygame.quit()
