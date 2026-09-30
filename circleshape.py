import pygame

class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...] = ()

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(self.containers)
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def wrap_around(self, width: int, height: int) -> None:
        if self.position.x < -self.radius:
            self.position.x = width + self.radius
        elif self.position.x > width + self.radius:
            self.position.x = -self.radius

        if self.position.y < -self.radius:
            self.position.y = height + self.radius
        elif self.position.y > height + self.radius:
            self.position.y = -self.radius

    def collides_with(self, other: "CircleShape") -> bool:
        distance = self.position.distance_to(other.position)
        return distance <= (self.radius + other.radius)

def point_in_triangle(p: pygame.Vector2, a: pygame.Vector2, b: pygame.Vector2, c: pygame.Vector2) -> bool:
    def sign(p1: pygame.Vector2, p2: pygame.Vector2, p3: pygame.Vector2) -> float:
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    d1 = sign(p, a, b)
    d2 = sign(p, b, c)
    d3 = sign(p, c, a)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)
