import sys
import random
import pygame
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particle import Particle
from powerup import ShieldPowerUp
from background import create_or_load_background
from leaderboard import load_leaderboard, save_score

LEVEL_SPECS = {
    1: {
        "title": "LEVEL 1",
        "speed_mult": 1.0,
        "spawn_mult": 1.0,
        "rules": [
            "Asteroids: Base Speed & Spawn Rate",
            "Shield 100%: Absorbs 5 hits of ANY size",
            "Survival Goal: Survive 120 seconds",
        ],
    },
    2: {
        "title": "LEVEL 2",
        "speed_mult": 1.10,
        "spawn_mult": 1.0,
        "rules": [
            "Asteroid Speed: +10%",
            "Shield 100%: 5 min-radius hits OR 1 max-radius hit",
            "Collect 'S' tokens to replenish shield (+25%)",
        ],
    },
    3: {
        "title": "LEVEL 3",
        "speed_mult": 1.10,
        "spawn_mult": 1.10,
        "rules": [
            "Asteroid Speed: +10% | Spawn Rate: +10%",
            "Shield 100%: 4 min-radius hits OR 1 max-radius hit",
            "Survival Goal: 120 seconds",
        ],
    },
    4: {
        "title": "LEVEL 4",
        "speed_mult": 1.20,
        "spawn_mult": 1.10,
        "rules": [
            "Asteroid Speed: +20% | Spawn Rate: +10%",
            "Shield 100%: 3 min-radius hits OR 1 max-radius hit",
            "Extreme hazard warning",
        ],
    },
    5: {
        "title": "LEVEL 5 - FINAL WAVE",
        "speed_mult": 1.25,
        "spawn_mult": 1.25,
        "rules": [
            "Asteroid Speed: +25% | Spawn Rate: +25%",
            "Shield 100%: 2 min-radius hits OR 1 max-radius hit",
            "Survive to conquer the sector!",
        ],
    },
}

def show_level_intro(screen: pygame.Surface, font_title: pygame.font.Font, font_body: pygame.font.Font, level: int) -> None:
    clock = pygame.time.Clock()
    spec = LEVEL_SPECS[level]
    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                waiting = False

        screen.fill((10, 15, 30))

        title_surf = font_title.render(spec["title"], True, (0, 240, 255))
        screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 180)))

        y = 280
        for rule in spec["rules"]:
            rule_surf = font_body.render(f"- {rule}", True, "white")
            screen.blit(rule_surf, (SCREEN_WIDTH // 2 - 250, y))
            y += 40

        prompt = font_body.render("Press SPACE to begin sector", True, (255, 215, 0))
        screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, 540)))

        pygame.display.flip()
        clock.tick(60)

def game_over_screen(screen: pygame.Surface, font_title: pygame.font.Font, font_body: pygame.font.Font, final_score: int) -> None:
    initials = ""
    clock = pygame.time.Clock()
    saved = False
    leaderboard = load_leaderboard()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not saved:
                    if event.key == pygame.K_BACKSPACE:
                        initials = initials[:-1]
                    elif event.key == pygame.K_RETURN and len(initials) in (2, 3):
                        leaderboard = save_score(initials, final_score)
                        saved = True
                    elif len(initials) < 3 and event.unicode.isalpha():
                        initials += event.unicode.upper()
                else:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        sys.exit()

        screen.fill((15, 10, 20))

        over_surf = font_title.render("GAME OVER", True, (255, 60, 60))
        screen.blit(over_surf, over_surf.get_rect(center=(SCREEN_WIDTH // 2, 70)))

        score_surf = font_body.render(f"Final Score: {final_score}", True, "white")
        screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH // 2, 120)))

        if not saved:
            prompt_surf = font_body.render(f"Enter 2-3 Initials: {initials}_", True, (255, 230, 90))
            screen.blit(prompt_surf, prompt_surf.get_rect(center=(SCREEN_WIDTH // 2, 165)))
            sub = font_body.render("(Press ENTER when finished)", True, (160, 160, 160))
            screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2, 200)))
        else:
            done_surf = font_body.render("Score recorded! Press ESC or ENTER to exit.", True, (100, 255, 100))
            screen.blit(done_surf, done_surf.get_rect(center=(SCREEN_WIDTH // 2, 175)))

        # Draw Top 10 Leaderboard
        lb_header = font_body.render("--- TOP 10 PILOTS ---", True, (0, 220, 255))
        screen.blit(lb_header, lb_header.get_rect(center=(SCREEN_WIDTH // 2, 250)))

        y_offset = 290
        for i, entry in enumerate(leaderboard[:10], start=1):
            row_text = f"{i:2d}. {entry['initials']:<3}  ...  {entry['score']:>6d}"
            row_surf = font_body.render(row_text, True, "white")
            screen.blit(row_surf, (SCREEN_WIDTH // 2 - 120, y_offset))
            y_offset += 32

        pygame.display.flip()
        clock.tick(60)

def main() -> None:
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font_hud = pygame.font.SysFont("monospace", 20)
    font_body = pygame.font.SysFont("monospace", 24)
    font_title = pygame.font.SysFont("monospace", 42, bold=True)
    bg_surface = create_or_load_background("background.png")

    clock = pygame.time.Clock()
    dt = 0.0

    current_level = 1
    level_time_remaining = 120.0
    score = 0
    lives = 3
    powerup_spawn_timer = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Particle.containers = (updatable, drawable)
    ShieldPowerUp.containers = (powerups, updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    def set_level(lvl: int) -> None:
        nonlocal level_time_remaining
        for a in list(asteroids):
            a.kill()
        for p in list(powerups):
            p.kill()
        for s in list(shots):
            s.kill()

        spec = LEVEL_SPECS[lvl]
        asteroid_field.set_level_modifiers(spec["speed_mult"], spec["spawn_mult"])
        level_time_remaining = 120.0
        player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        show_level_intro(screen, font_title, font_body, lvl)

    set_level(current_level)

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # Advance level timer
        level_time_remaining -= dt
        if level_time_remaining <= 0:
            current_level += 1
            if current_level > 5:
                # Victory completion
                game_over_screen(screen, font_title, font_body, score)
                return
            set_level(current_level)
        # Periodic shield token spawning (every 18 seconds)
        powerup_spawn_timer += dt
        if powerup_spawn_timer >= 18.0:
            powerup_spawn_timer = 0.0
            p = ShieldPowerUp(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
            p.velocity = pygame.Vector2(random.uniform(-30, 30), random.uniform(-30, 30))

        updatable.update(dt)
        # Collect Shield Power-ups
        for pup in powerups:
            if pup.collides_with(player):
                player.shield_pct = min(100.0, player.shield_pct + 25.0)
                pup.kill()
        # Ship-to-asteroid collision handling with shield depletion
        ship_triangle = player.triangle()
        for asteroid in asteroids:
            if player.invulnerable_timer <= 0 and asteroid.collides_with_triangle(ship_triangle):
                log_event("player_hit")
                damage = player.calculate_shield_damage(asteroid.radius, current_level)
                if player.shield_pct > 0:
                    player.shield_pct = max(0.0, player.shield_pct - damage)
                    asteroid.split()
                else:
                    lives -= 1
                    if lives <= 0:
                        game_over_screen(screen, font_title, font_body, score)
                        return
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
        # Draw Frame
        screen.blit(bg_surface, (0, 0))

        for entity in drawable:
            entity.draw(screen)

        # Display HUD
        minutes = int(level_time_remaining) // 60
        seconds = int(level_time_remaining) % 60
        timer_str = f"Time: {minutes:02d}:{seconds:02d}"

        screen.blit(font_hud.render(f"Lvl: {current_level}/5 | Score: {score}", True, "white"), (20, 20))
        screen.blit(font_hud.render(f"Lives: {lives} | Shield: {int(player.shield_pct)}%", True, (0, 220, 255)), (20, 46))
        screen.blit(font_hud.render(f"Weapon: {player.weapon_mode} (1-3)", True, "white"), (20, 72))
        screen.blit(font_hud.render(timer_str, True, (255, 215, 0)), (SCREEN_WIDTH - 180, 20))

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
