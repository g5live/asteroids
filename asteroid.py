import math
import random
import pygame
from circleshape import CircleShape, point_in_triangle
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_event
from particle import Particle

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.vertex_count = random.randint(8, 12)
        # Generate irregular offset distances for each vertex to make it lumpy
        self.offsets = [random.uniform(0.75, 1.25) for _ in range(self.vertex_count)]

    def get_polygon_points(self) -> list[pygame.Vector2]:
        points = []
        angle_step = 360 / self.vertex_count
        for i in range(self.vertex_count):
            angle = math.radians(i * angle_step)
            r = self.radius * self.offsets[i]
            offset_vec = pygame.Vector2(math.cos(angle) * r, math.sin(angle) * r)
            points.append(self.position + offset_vec)
        return points

    def draw(self, screen: pygame.Surface) -> None:
        points = self.get_polygon_points()
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.wrap_around(SCREEN_WIDTH, SCREEN_HEIGHT)

    def collides_with_triangle(self, tri: list[pygame.Vector2]) -> bool:
        # Check if the asteroid center or any vertices are inside the ship triangle
        a, b, c = tri[0], tri[1], tri[2]
        if point_in_triangle(self.position, a, b, c):
            return True
        # Check if any ship triangle vertices are inside the asteroid circle
        for pt in tri:
            if self.position.distance_to(pt) <= self.radius:
                return True
        return False

    def create_explosion(self, count: int = 15) -> None:
        for _ in range(count):
            Particle(self.position.x, self.position.y)

    def split(self) -> None:
        self.kill()
        self.create_explosion(count=15)
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")

        random_angle = random.uniform(20, 50)
        vel1 = self.velocity.rotate(random_angle)
        vel2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_1.velocity = vel1 * 1.2
        new_asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_2.velocity = vel2 * 1.2