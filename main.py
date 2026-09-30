import sys
import pygame
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particle import Particle
from background import create_or_load_background

def main() -> None:
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont("monospace", 22)
    bg_surface = create_or_load_background("background.png")

    clock = pygame.time.Clock()
    dt = 0.0

    score = 0
    lives = 5

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        # Ship-to-asteroid collision using exact triangular hitbox
        ship_triangle = player.triangle()
        for asteroid in asteroids:
            if player.invulnerable_timer <= 0 and asteroid.collides_with_triangle(ship_triangle):
                log_event("player_hit")
                lives -= 1
                if lives <= 0:
                    print(f"Game over! Final Score: {score}")
                    sys.exit()
                else:
                    player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    if asteroid.radius <= ASTEROID_MIN_RADIUS:
                        score += 100
                    elif asteroid.radius <= ASTEROID_MIN_RADIUS * 2:
                        score += 50
                    else:
                        score += 20
                    asteroid.split()
                    shot.kill()
        # Render background and objects
        screen.blit(bg_surface, (0, 0))

        for entity in drawable:
            entity.draw(screen)
        # HUD overlay
        score_surface = font.render(f"Score: {score}", True, "white")
        lives_surface = font.render(f"Lives: {lives}", True, "white")
        weapon_surface = font.render(f"Weapon: {player.weapon_mode} (Keys 1-3)", True, "white")

        screen.blit(score_surface, (20, 20))
        screen.blit(lives_surface, (20, 48))
        screen.blit(weapon_surface, (20, 76))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
