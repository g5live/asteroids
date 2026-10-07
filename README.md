![G5LIVE — Build · Understand · Apply](assets/brand/g5live.svg)

# Asteroids

A Python/Pygame game started through Boot.dev's guided Asteroids project, then extended with weapons, shields, scoring and a five-level survival campaign.

**Build · Understand · Apply.** It gives me a practical way to explore Python classes, vectors, collisions and game state. Further development is an optional side project alongside my main cybersecurity goals.

## Run the game

Requires Python **3.13+**, `uv` and a graphical desktop. The project uses Pygame **2.6.1**.

```bash
git clone https://github.com/g5live/asteroids.git
cd asteroids
uv sync
uv run main.py
```

Boot.dev CLI login is not needed to play.

## Controls

| Key | Action |
|---|---|
| W / S | Move forwards / backwards |
| A / D | Rotate |
| Space | Fire |
| 1 / 2 / 3 | Single / Spread / Sniper weapon |
| Space or Enter | Start the next level briefing |
| Close window | Quit |

At the score screen, enter **2–3 initials** and press Enter to save. Backspace corrects them; after saving, Enter or Escape exits.

## What works today

- Five increasingly demanding levels, each lasting 120 seconds.
- Three starting lives, shields and brief invulnerability after respawning.
- Three weapons with different patterns, speeds and cooldowns.
- Shield pickups restoring 25 percentage points, capped at 100%.
- Irregular asteroid shapes, explosion particles and screen wrapping for the ship/asteroids.
- Scoring: small asteroids 100 points, medium 50 and large 20.
- A local top-10 leaderboard saved in `leaderboard.json` in the working directory.

Survive a level to advance; losing all lives ends the run. Shields reset at each level and respawn. Later levels increase asteroid speed/spawn frequency and make larger asteroids more damaging. A hit depleting the shield does not itself cost a life; a later hit with no shield does.

Use the same working directory to retain the same leaderboard. Add `background.png` there for a custom background; otherwise a starfield is generated.

## Current limits and next steps

This is a desktop game; mobile controls, packaged downloads and multiplayer are not implemented. Ship collision checks use a triangle, while asteroids still use simplified radius-based geometry.

Next useful work is pause/restart, clearer settings, more reliable score storage and tests for collisions, shields and level changes. More environments, weapon limits, mobile support and two-device play remain later ideas.

`main.py` manages the campaign; player, asteroid, projectile, pickup and leaderboard modules keep the main behaviours separate. Packaging and platform claims need testing before a release.

Part of the G5LIVE app family. See the [brand guide](assets/brand/BRAND.md) and [release-readiness notes](docs/RELEASE_READINESS.md).
