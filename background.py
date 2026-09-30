import os
import random
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

def create_or_load_background(filename: str = "background.png") -> pygame.Surface:
    if os.path.exists(filename):
        image = pygame.image.load(filename).convert()
        return pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Procedural deep-space background with layered stars and nebula dust
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface.fill((8, 10, 20))
    # Faint space dust
    for _ in range(8):
        cloud_surf = pygame.Surface((300, 300), pygame.SRCALPHA)
        color = random.choice([(25, 15, 45, 18), (15, 30, 45, 18), (20, 40, 30, 18)])
        pygame.draw.circle(cloud_surf, color, (150, 150), 140)
        surface.blit(cloud_surf, (random.randint(-100, SCREEN_WIDTH), random.randint(-100, SCREEN_HEIGHT)))
    # Distant stars
    for _ in range(120):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        brightness = random.randint(120, 255)
        radius = random.choice([1, 1, 1, 2])
        pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), radius)

    return surface
