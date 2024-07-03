import pygame

# Define a range of gray colors using RGB values
dark_gray = (50, 50, 50)
medium_gray = (128, 128, 128)
light_gray = (250, 250, 250)


# Example of using gray color ranges in Pygame
def is_gray(pixel_color):
    # Check if the pixel color is within the defined gray ranges
    if (dark_gray[0] <= pixel_color.r <= dark_gray[0] and
            dark_gray[1] <= pixel_color.g <= dark_gray[1] and
            dark_gray[2] <= pixel_color.b <= dark_gray[2]):
        return True

    if (medium_gray[0] <= pixel_color.r <= medium_gray[0] and
            medium_gray[1] <= pixel_color.g <= medium_gray[1] and
            medium_gray[2] <= pixel_color.b <= medium_gray[2]):
        return True

    if (dark_gray[0] <= pixel_color.r <= light_gray[0] and
            dark_gray[1] <= pixel_color.g <= light_gray[1] and
            dark_gray[2] <= pixel_color.b <= light_gray[2]):
        return True

    return False


def check_road(x,y):
    # Example usage
    map_img = pygame.image.load("files/map.png")
    pixel_color = map_img.get_at((x, y))
    # print(pixel_color)
    pixel_color= (pixel_color.r, pixel_color.g, pixel_color.b)

    if pixel_color == (245, 240, 229):
        # Do something when the pixel color matches any of the gray ranges
        return True
    else:
        # print("not on road")
        return False
