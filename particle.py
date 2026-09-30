import random
import pygame


class Particle(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...] = ()

    def __init__(self, x: float, y: float) -> None:
        super().__init__(self.containers)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * random.uniform(50, 180)
        self.lifetime = random.uniform(0.3, 0.6)
        self.age = 0.0

    def update(self, dt: float) -> None:
        self.age += dt
        if self.age >= self.lifetime:
            self.kill()
            return
        self.position += self.velocity * dt

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", (int(self.position.x), int(self.position.y)), 1)
