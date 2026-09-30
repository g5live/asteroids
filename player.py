import pygame
from circleshape import CircleShape
from shot import Shot
from constants import (
    PLAYER_RADIUS,
    TURN_SPEED,
    PLAYER_SPEED,
    SHOT_SPEED,
    SHOT_COOLDOWN_SECONDS,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    LINE_WIDTH,
)

class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0.0
        self.invulnerable_timer = 0.0
        self.weapon_mode = "Single"  # Available: "Single", "Spread", "Sniper"

    def respawn(self, x: float, y: float) -> None:
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.invulnerable_timer = 3.0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        if self.invulnerable_timer > 0 and int(self.invulnerable_timer * 10) % 2 == 0:
            return
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt: float) -> None:
        self.rotation += TURN_SPEED * dt

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        if self.shoot_timer > 0:
            return

        direction = pygame.Vector2(0, 1).rotate(self.rotation)

        if self.weapon_mode == "Single":
            self.shoot_timer = SHOT_COOLDOWN_SECONDS
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = direction * SHOT_SPEED

        elif self.weapon_mode == "Spread":
            self.shoot_timer = SHOT_COOLDOWN_SECONDS * 1.8
            for angle in (-15, 0, 15):
                shot = Shot(self.position.x, self.position.y, radius=4, color="yellow")
                shot.velocity = direction.rotate(angle) * (SHOT_SPEED * 0.9)

        elif self.weapon_mode == "Sniper":
            self.shoot_timer = SHOT_COOLDOWN_SECONDS * 3.0
            shot = Shot(self.position.x, self.position.y, radius=7, color="cyan")
            shot.velocity = direction * (SHOT_SPEED * 1.8)

    def update(self, dt: float) -> None:
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt

        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        # Weapon Selection
        if keys[pygame.K_1]:
            self.weapon_mode = "Single"
        elif keys[pygame.K_2]:
            self.weapon_mode = "Spread"
        elif keys[pygame.K_3]:
            self.weapon_mode = "Sniper"

        self.wrap_around(SCREEN_WIDTH, SCREEN_HEIGHT)