#!/usr/bin/env python3
"""
scraper_connector.py - Hephaestus Factory Scraper Connector
Connects to Artemis symbiote for artist leads & reports
Feeds data to populate empire pillars
"""

import subprocess
import json
import os
import time
from datetime import datetime
import requests
from pathlib import Path

# ────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────
# Path to symbiote.py in your Artemis repo (UPDATE THIS!)
ARTEMIS_REPO_PATH = Path("/path/to/your/Architect-Artemis")  # ← CHANGE THIS (absolute or relative)
SYMBIOTE_SCRIPT = ARTEMIS_REPO_PATH / "symbiote.py"

# Stewardship dir inside Artemis repo
STEWARDSHIP_DIR = ARTEMIS_REPO_PATH / "creator-creation" / "stewardship"

# Council fallback URL (if subprocess fails)
ARTEMIS_URL = "https://architect-artemis.vercel.app/api/transmit"

# Output feeds in hephaestus-factory
FEED_DIR = Path("feeds")
ARTIST_FEED_DIR = FEED_DIR / "artist_leads"
os.makedirs(ARTIST_FEED_DIR, exist_ok=True)

def run_symbiote_discovery(genre=None, limit=10, min_nurture=7):
    """Run symbiote.py discover-artists and get the latest leads file"""
    if not SYMBIOTE_SCRIPT.exists():
        print(f"❌ Symbiote script not found at: {SYMBIOTE_SCRIPT}")
        print("Update ARTEMIS_REPO_PATH in scraper_connector.py")
        return None, None

    cmd = [
        "python3", str(SYMBIOTE_SCRIPT),
        "discover-artists",
        "--limit", str(limit),
        "--min-nurture", str(min_nurture)
    ]
    if genre:
        cmd.extend(["--genre", genre])

    print(f"Running Artemis discovery: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Symbiote stdout:\n", result.stdout.strip())
        if result.stderr:
            print("Symbiote stderr:\n", result.stderr.strip())

        # Find latest artist_leads_*.json
        files = [f for f in STEWARDSHIP_DIR.glob("artist_leads_*.json")]
        if not files:
            print("No artist_leads_*.json found in stewardship")
            return None, None

        latest_file = max(files, key=lambda p: p.stat().st_mtime)
        with open(latest_file, 'r') as f:
            leads = json.load(f)

        print(f"✅ Loaded {len(leads)} artist leads from {latest_file.name}")
        return leads, str(latest_file)
    except subprocess.CalledProcessError as e:
        print("Symbiote failed:", e.stderr.strip())
        return None, None
    except Exception as e:
        print(f"Error running symbiote: {e}")
        return None, None

def fallback_council_query(query_type="artist_leads"):
    """Fallback: Direct Council query if subprocess fails"""
    payload = {
        "prompt": f"Generate {query_type} for empire pillars. Focus on artist leads and site optimizations. Output JSON array.",
        "handshake": "dad"
    }
    try:
        response = requests.post(ARTEMIS_URL, json=payload, timeout=30)
        if response.status_code == 200:
            raw = response.json().get('verdict', '[]')
            leads = json.loads(raw) if raw else []
            print(f"✅ Fallback Council returned {len(leads)} items")
            return leads
        else:
            print(f"❌ Council fallback failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Council fallback error: {e}")
        return []

def populate_pillar_from_leads(pillar_slug="sonic-stage", leads=None, feed_file=None):
    """Populate target pillar repo with artist data (simulated for now)"""
    if not leads:
        print("No leads to populate")
        return

    print(f"\nPopulating pillar: {pillar_slug}")
    for lead in leads:
        artist_name = lead.get("name", "Unknown").replace(" ", "_").lower()
        file_path = f"artists/{artist_name}.json"
        content = json.dumps(lead, indent=2)

        print(f"  → Would create/update {file_path} with:")
        print(f"    {content[:120]}..." if len(content) > 120 else content)

        # TODO: Real GitHub API population (next step)
        # octokit.repos.create_or_update_file_contents(...)
        time.sleep(0.3)  # Visual pacing

    print(f"✅ Simulated population of {len(leads)} artists into {pillar_slug}")
    # Future: Commit changes to the pillar repo

if __name__ == "__main__":
    print("Hephaestus Factory Scraper Connector - Starting...")
    print(f"Artemis symbiote path: {SYMBIOTE_SCRIPT}")

    # Step 1: Try symbiote subprocess (preferred)
    leads, latest_feed = run_symbiote_discovery(
        genre="indie electronic",
        limit=8,
        min_nurture=7
    )

    # Step 2: Fallback to direct Council if subprocess failed
    if not leads:
        print("Subprocess failed - falling back to direct Council query")
        leads = fallback_council_query("artist_leads")

    # Step 3: Populate example pillar
    if leads:
        populate_pillar_from_leads("sonic-stage", leads, latest_feed)
    else:
        print("No leads discovered - check symbiote logs or Council status")
