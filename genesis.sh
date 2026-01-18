#!/bin/bash
# genesis.sh - Hephaestus Factory Bootstrap

echo "Hephaestus Factory Genesis - Building the Empire Engine"

# Install deps
npm install
pip install -r requirements.txt

# Create pillar_manifest.json if missing
if [ ! -f pillar_manifest.json ]; then
  echo "Creating pillar manifest..."
  # Use the JSON from my previous message
  cat > pillar_manifest.json << 'EOF'
  {
    "pillars": [
      {
        "name": "Hephaestus Factory",
        "repo_slug": "hephaestus-factory",
        "core_purpose": "The master engine that builds and populates new repositories via GitHub API, manages the empire's creation, and connects to global scraper for data feeds.",
        "tech_stack": "Node.js, Python, GitHub API (Octokit), Cron for scheduling",
        "initial_files": [
          "package.json",
          "README.md",
          "hephaestus.js (main script for repo creation/population)",
          "pillar_manifest.json (JSON blueprint for all pillars)",
          "env.example",
          ".gitignore",
          "genesis.sh (bootstrap script)"
        ],
        "priority": 1,
        "dependencies": "None (foundational)"
      },
      {
        "name": "Sovereign Midas",
        "repo_slug": "sovereign-midas",
        "core_purpose": "Centralize the Midas Protocol: 3D assets, gold HEX codes (#d4af37), personality logic, and branding standards for the empire's visual DNA.",
        "tech_stack": "Three.js for 3D assets, CSS/HEX for colors, JSON for personality configs",
        "initial_files": [
          "README.md",
          "midas_protocol.json (core DNA blueprint)",
          "assets/ (3D models, textures)",
          "personality.py (logic for Midas AI persona)",
          "gold_hex.css (styling standards)"
        ],
        "priority": 2,
        "dependencies": "Used by all pillars for branding"
      },
      // ... (all 15 pillars from my previous message)
    ]
  }
  EOF
fi

echo "Factory ready. Run 'npm run spawn-all' to build the empire."
