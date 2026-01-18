// factory.js - Hephaestus Factory Main Engine
// Spawns repos and populates with initial files from manifest

require('dotenv').config();
const { Octokit } = require('@octokit/rest');
const fs = require('fs-extra');
const path = require('path');

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

const manifest = JSON.parse(fs.readFileSync('pillar_manifest.json', 'utf8'));
const BASE_REPO_NAME = process.env.BASE_ORG || 'yourusername';  // e.g., 'olympus-empire'

async function spawnRepo(pillar) {
  try {
    // Create repo
    const repo = await octokit.repos.createForAuthenticatedUser({
      name: pillar.repo_slug,
      description: pillar.core_purpose,
      private: pillar.priority > 1,  // Private for non-foundational
      auto_init: true
    });
    console.log(`✅ Created repo: ${repo.data.full_name}`);

    // Clone locally (temp)
    const tempDir = path.join(__dirname, 'temp-clone', pillar.repo_slug);
    await fs.ensureDir(tempDir);
    // (Use child_process to git clone, or use Octokit to upload files directly)

    // Populate initial files
    for (const file of pillar.initial_files) {
      let content = `// Placeholder for ${file}\n`;
      if (file.endsWith('.json')) content = JSON.stringify({}, null, 2);
      if (file.endsWith('.md')) content = `# ${pillar.name}\n\n${pillar.core_purpose}`;
      
      await octokit.repos.createOrUpdateFileContents({
        owner: BASE_REPO_NAME,
        repo: pillar.repo_slug,
        path: file,
        message: `Initial: ${file}`,
        content: Buffer.from(content).toString('base64')
      });
      console.log(`📄 Populated: ${file}`);
    }

    return repo.data.full_name;
  } catch (error) {
    console.error(`❌ Failed to spawn ${pillar.name}:`, error.message);
  }
}

async function spawnAll() {
  for (const pillar of manifest.pillars.sort((a, b) => a.priority - b.priority)) {
    if (pillar.priority === 1) continue;  // Skip self
    await spawnRepo(pillar);
  }
  console.log('Empire built!');
}

const args = process.argv.slice(2);
if (args.includes('spawn-all')) {
  spawnAll();
} else if (args.includes('spawn') && args.includes('--pillar')) {
  const pillarName = args[args.indexOf('--pillar') + 1];
  const pillar = manifest.pillars.find(p => p.name === pillarName);
  if (pillar) spawnRepo(pillar);
} else {
  console.log('Usage: node factory.js spawn --pillar=Sonic Stage');
}
