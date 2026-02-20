#!/usr/bin/env node
/**
 * Prebuild script — reads all lab YAML files and writes a single
 * lab-data.json that the SvelteKit app imports at build time.
 *
 * Runs before `vite build` so the data is baked into the deployment.
 * This means every git push (which triggers a Vercel rebuild) picks
 * up the latest lab state automatically.
 */

import { readFileSync, readdirSync, existsSync, statSync, writeFileSync, mkdirSync } from 'fs';
import { join, resolve } from 'path';
import YAML from 'yaml';

const LAB_ROOT = process.env.LAB_ROOT || resolve(process.cwd(), '..');

function readYaml(path) {
	try {
		return YAML.parse(readFileSync(path, 'utf-8'));
	} catch { return null; }
}

function readMd(path) {
	try { return readFileSync(path, 'utf-8'); }
	catch { return null; }
}

function loadDir(dir, ext, parser) {
	if (!existsSync(dir)) return [];
	return readdirSync(dir)
		.filter(f => f.endsWith(ext))
		.sort()
		.map(f => parser(join(dir, f), f))
		.filter(Boolean);
}

// --- Load everything ---
const config = readYaml(join(LAB_ROOT, 'lab.yaml'));
const findingsData = readYaml(join(LAB_ROOT, 'knowledge', 'findings.yaml'));
const hypothesesData = readYaml(join(LAB_ROOT, 'knowledge', 'hypotheses.yaml'));
const deadEndsData = readYaml(join(LAB_ROOT, 'knowledge', 'dead_ends.yaml'));
const changelogData = readYaml(join(LAB_ROOT, 'changelog.yaml'));

const experiments = (() => {
	const dir = join(LAB_ROOT, 'experiments');
	if (!existsSync(dir)) return [];
	return readdirSync(dir)
		.filter(e => { try { return statSync(join(dir, e)).isDirectory(); } catch { return false; } })
		.sort()
		.map(name => ({
			id: name,
			name,
			status: readYaml(join(dir, name, 'status.yaml')),
			analysis: readMd(join(dir, name, 'analysis.md')),
			hypothesis: readMd(join(dir, name, 'hypothesis.md')),
		}));
})();

const feedback = loadDir(join(LAB_ROOT, 'feedback'), '.yaml', (path) => readYaml(path));

const workflows = loadDir(join(LAB_ROOT, 'workflows'), '.yaml', (path, filename) => {
	const wf = readYaml(path);
	if (wf) wf.filename = filename;
	return wf;
});

const readme = readMd(join(LAB_ROOT, 'CLAUDE.md'));

const labData = {
	config,
	findings: findingsData?.findings ?? [],
	hypotheses: hypothesesData?.hypotheses ?? [],
	dead_ends: deadEndsData?.dead_ends ?? [],
	experiments,
	feedback,
	changelog: changelogData?.changes ?? [],
	workflows,
	readme,
};

// Write to src/lib so SvelteKit can import it
const outDir = join(process.cwd(), 'src', 'lib');
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'lab-data.json'), JSON.stringify(labData, null, 2));

console.log(`Prebuild complete — wrote lab-data.json`);
console.log(`  LAB_ROOT: ${LAB_ROOT}`);
console.log(`  Config: ${config?.name ?? 'not found'}`);
console.log(`  Findings: ${labData.findings.length}`);
console.log(`  Hypotheses: ${labData.hypotheses.length}`);
console.log(`  Experiments: ${labData.experiments.length}`);
console.log(`  Workflows: ${labData.workflows.length}`);
console.log(`  Feedback: ${labData.feedback.length}`);
