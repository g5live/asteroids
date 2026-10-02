# Release readiness — asteroids

Review date: 2 October 2026. Proposed work, not an implementation or release announcement.

## Appropriate next functionality

- Add pause/restart, clearer controls/settings, optional audio and persistent user preferences.
- Separate campaign state and scoring from rendering to make them testable. Improve leaderboard corruption handling and use a predictable user-data location.
- Develop additional settings and weapon-use limits after the core desktop experience is stable. Mobile support and two-device multiplayer are separate later projects.

## Before a first public release

- Replace placeholder package metadata, record code/artwork/audio provenance and clarify reuse permissions.
- Test collision/scoring, shields, level transitions and persistence; add headless smoke checks and manual play-test notes.
- Test desktop packaging and downloadable builds on each claimed OS. Do not claim mobile support until touch controls, packaging and device testing exist.
- Keep personal scores/logs out of release assets and the repository. Publish controls, screenshots, dependencies, platform limits and known issues.

## Shared release preparation

Before publishing a tagged release, choose a project licence after reviewing tutorial and asset provenance; document installation, supported versions, examples and known limits; add a changelog, issue/PR templates, contribution guidance and a vulnerability-reporting policy; run CI on the claimed platforms and test a clean installation. Add dependency updates and appropriate repository security checks where supported. Provide tagged release notes and usable download assets where relevant. These are readiness recommendations, not GitHub certification or features already delivered.

GitHub references: [community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file) and [releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).
