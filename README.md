# Hephaestus Factory

The master engine for Project Olympus Empire. Spawns and populates the 15 pillar repositories based on the pillar_manifest.json blueprint.

## Setup
1. Clone: `git clone https://github.com/yourusername/hephaestus-factory.git`
2. `npm install` (Node)
3. `pip install -r requirements.txt` (Python)
4. Copy `.env.example` to `.env` and fill in keys
5. Run: `npm run spawn-all` (creates all pillars) or `npm start -- --pillar=sonic-stage` (one at a time)

## Commands
- `npm run spawn-all` — Create all 15 pillar repos
- `npm start -- --pillar=sonic-stage` — Spawn one pillar
- `npm run populate -- --repo=sovereign-midas` — Populate an existing repo with files
- `npm run test` — Dry run/test mode

## Pillar Manifest
See `pillar_manifest.json` for blueprint of all 15 pillars (priority, files, deps).

Built by Olympus By Merlin $Dropee — January 18, 2026
