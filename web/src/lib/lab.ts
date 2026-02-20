/**
 * Lab data loader — imports pre-built JSON from prebuild.js.
 *
 * At build time, prebuild.js reads all YAML files from the lab repo
 * and writes lab-data.json. This module re-exports that data with types.
 *
 * This approach works on any hosting (Vercel, static, local dev) because
 * the data is baked into the build. Every git push triggers a rebuild,
 * so the dashboard always reflects the latest lab state.
 */

import labData from './lab-data.json';

// --- Type definitions ---

export interface LabConfig {
	name: string;
	domain: string;
	mission: string;
	research_questions?: { id: string; question: string; status: string; priority: string }[];
	constraints?: Record<string, unknown>;
	evolution?: Record<string, unknown>;
	priority?: string[];
	[key: string]: unknown;
}

export interface Finding {
	id: string;
	date: string;
	statement: string;
	source?: string;
	evidence?: string[];
	evidence_type?: string;
	confidence: string;
	limitations?: string;
	needs?: string;
}

export interface Hypothesis {
	id: string;
	status: string;
	statement: string;
	rationale?: string;
	priority?: string;
	related_rq?: string;
	suggested_experiments?: string[];
	supporting?: string[];
}

export interface DeadEnd {
	id: string;
	date: string;
	what: string;
	why_failed: string;
	lesson: string;
	experiments?: string[];
}

export interface ExperimentStatus {
	status: string;
	agent?: string;
	started?: string;
	completed?: string;
	workflow?: string;
	hypothesis_ref?: string;
	outcome?: string;
	summary?: string;
}

export interface Experiment {
	id: string;
	name: string;
	status: ExperimentStatus | null;
	analysis: string | null;
	hypothesis: string | null;
}

export interface Feedback {
	from: string;
	date: string;
	type: string;
	regarding: string;
	comment: string;
	actionable?: boolean;
	suggested_action?: string;
}

export interface ChangelogEntry {
	id: string;
	date: string;
	type: string;
	target: string;
	proposed_by: string;
	approved_by: string;
	rationale: string;
	pr?: string;
}

export interface Workflow {
	name: string;
	description: string;
	filename: string;
	steps?: Record<string, unknown>;
	[key: string]: unknown;
}

export interface LabData {
	config: LabConfig | null;
	findings: Finding[];
	hypotheses: Hypothesis[];
	dead_ends: DeadEnd[];
	experiments: Experiment[];
	feedback: Feedback[];
	changelog: ChangelogEntry[];
	workflows: Workflow[];
	readme: string | null;
}

const data = labData as unknown as LabData;

export function getLabConfig(): LabConfig | null { return data.config; }
export function getFindings(): Finding[] { return data.findings; }
export function getHypotheses(): Hypothesis[] { return data.hypotheses; }
export function getDeadEnds(): DeadEnd[] { return data.dead_ends; }
export function getExperiments(): Experiment[] { return data.experiments; }
export function getExperiment(id: string): Experiment | null {
	return data.experiments.find(e => e.id === id) ?? null;
}
export function getFeedback(): Feedback[] { return data.feedback; }
export function getChangelog(): ChangelogEntry[] { return data.changelog; }
export function getWorkflows(): Workflow[] { return data.workflows; }
export function getReadme(): string | null { return data.readme; }
export function getAllLabData(): LabData { return data; }
