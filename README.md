# Asteroids

A Python/Pygame arcade game started through Boot.dev's [Build Asteroids using Python and Pygame](https://www.boot.dev/courses/build-asteroids-python) guided project, then extended with scoring, weapons, effects and a five-level survival campaign.

The course provided practice with multi-file Python projects, object-oriented programming, sprite groups, vectors, game loops and collision detection. The developments below build on that foundation.

## Run the game

Requires Python **3.13+**, [uv](https://docs.astral.sh/uv/) and a graphical desktop. Pygame **2.6.1** is pinned in the project dependencies.

```bash
git clone https://github.com/g5live/asteroids.git
cd asteroids
uv sync
uv run main.py
```

For an existing checkout, run the last two commands from its project directory. Boot.dev CLI login is not required to play.

## Controls

| Key | Action |
| --- | --- |
| `W` / `S` | Move forwards / backwards |
| `A` / `D` | Rotate left / right |
| `Space` | Fire |
| `1` | Single shot |
| `2` | Three-shot spread |
| `3` | Faster sniper projectile with a longer firing cooldown |
| Close window | Quit |

Press **Space or Enter** to start each level. At game over, enter **2–3 initials**, use Backspace to correct them, then Enter to save. After saving, Enter or Escape exits.

## Developments after the guided project

- **Scoring:** small asteroids award 100 points, medium 50 and large 20 when shot.
- **Multiple lives and respawning:** return to the centre with a short invulnerability period after losing a life.
- **Explosion effects:** particles appear when asteroids break apart.
- **Screen wrapping:** the ship and asteroids wrap around the play area; shots still despawn off-screen.
- **Background image support:** place `background.png` in the project directory to use your own image. Without one, the game generates a starfield and space-dust background.
- **Weapon types:** Single, Spread and Sniper have different projectile patterns, speeds and cooldowns.
- **Lumpy asteroids:** irregular polygon outlines replace perfect circles visually.
- **Triangular ship hitbox:** collision checks use the ship's triangle rather than only a circular player boundary. Asteroid collision geometry remains radius-based, with simplified triangle overlap checks.
- **Shields:** the campaign adds a visible shield with damage scaled by level and asteroid size.
- **Five levels:** increasingly demanding asteroid speed, spawn frequency and shield rules.
- **Collectable shield tokens:** `S` pickups restore 25 percentage points, capped at 100%; new tokens spawn periodically, approximately every 18 seconds of play.
- **Level briefings:** quick rules/status appear before each level.
- **Timed survival:** each level lasts up to 120 seconds; survive the timer to advance, or end the run when all lives are lost.
- **Persistent leaderboard:** a local top 10 with 2–3 initials after game over or completing Level 5.

## Five-level campaign rules

The campaign starts with **three lives**. Each level begins with a full shield, and respawning also restores the shield with a short invulnerability period.

All speed and spawn-frequency changes below are relative to the **Level 1 baseline**, not cumulative increases from the previous level.

| Level | Asteroid speed | Spawn frequency | Full shield absorbs | Duration |
| --- | --- | --- | --- | --- |
| 1 | Slow/base speed | Base rate | 5 hits of any asteroid size | 120 seconds |
| 2 | +10% | Base rate | 5 minimum-radius hits or 1 maximum-radius hit | 120 seconds |
| 3 | +10% | +10% | 4 minimum-radius hits or 1 maximum-radius hit | 120 seconds |
| 4 | +20% | +10% | 3 minimum-radius hits or 1 maximum-radius hit | 120 seconds |
| 5 | +25% | +25% | 2 minimum-radius hits or 1 maximum-radius hit | 120 seconds |

On Levels 2–5, intermediate asteroid sizes cause proportionally scaled shield damage. These hit counts describe shield depletion: a collision while shield remains reduces it to a minimum of zero; a subsequent collision with no shield costs a life. Shield pickups can extend survival.

The baseline spawns an asteroid approximately every 0.8 seconds; a higher spawn-frequency multiplier shortens that interval. Asteroid fragments also accelerate when split.

### Leaderboard storage

The campaign saves the top 10 scores to `leaderboard.json` in the working directory. Run from the same project directory to keep using the same table. Scores persist between launches while that file remains available; this is a local leaderboard, not an online service or cloud backup.

## Project layout

| File | Responsibility |
| --- | --- |
| `main.py` | Game loop, collisions, scoring and game state and campaign screens |
| `player.py` | Movement, weapons, ship geometry and respawning and shield logic |
| `asteroid.py` / `asteroidfield.py` | Asteroid appearance, splitting and spawning |
| `circleshape.py` | Shared sprite geometry and movement helpers |
| `shot.py` / `particle.py` | Projectiles and explosion particles |
| `background.py` | Load a background image or generate a starfield |
| `constants.py` | Screen dimensions and base tuning values |
| `logger.py` | Game event/state logging |
| `powerup.py` / `leaderboard.py` | Shield pickups and score persistence |

## Future development

- Additional levels in different settings.
- Weapon-use limits, such as ammunition or energy constraints.
- Android and Apple mobile compatibility (iOS/iPadOS), including suitable controls and packaging.
- Two-player connectivity across two devices.

These are planned features, not currently supported capabilities.
