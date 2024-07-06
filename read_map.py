import pygame

BLACK = (0, 0, 0)


# Example of using gray color ranges in Pygame
def check_road(x, y):
    # Example usage
    map_img = pygame.image.load("files/map_avi.png")
    pixel_color = map_img.get_at((x, y))
    pixel_color = (pixel_color.r, pixel_color.g, pixel_color.b)

    if BLACK == pixel_color:
        return True
    else:
        return False
