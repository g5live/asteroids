import pygame
from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, LINE_WIDTH, SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self, x: float, y: float, radius: float = SHOT_RADIUS, color: str = "white") -> None:
        super().__init__(x, y, radius)
        self.color = color

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        # Despawn shots if they move well off-screen rather than looping indefinitely
        if (
            self.position.x < -50
            or self.position.x > SCREEN_WIDTH + 50
            or self.position.y < -50
            or self.position.y > SCREEN_HEIGHT + 50
        ):
            self.kill()
