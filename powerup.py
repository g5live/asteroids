import pygame
from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class ShieldPowerUp(CircleShape):
    containers: tuple[pygame.sprite.Group, ...] = ()

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, radius=12)
        self.pulse = 0.0

    def draw(self, screen: pygame.Surface) -> None:
        # Draw glowing layered shield token
        pygame.draw.circle(screen, (0, 220, 255), self.position, self.radius, 2)
        pygame.draw.circle(screen, (100, 255, 255), self.position, self.radius - 4, 1)
        font = pygame.font.SysFont("monospace", 12, bold=True)
        text = font.render("S", True, (0, 240, 255))
        rect = text.get_rect(center=(self.position.x, self.position.y))
        screen.blit(text, rect)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.wrap_around(SCREEN_WIDTH, SCREEN_HEIGHT)
