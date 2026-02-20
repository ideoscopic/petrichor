/**
 * Feed system — transforms lab data into a unified activity stream.
 *
 * Every lab event (experiment, finding, feedback, changelog entry, dead end)
 * becomes a FeedItem with action buttons linking to GitHub.
 */

import type { Experiment, Finding, Feedback, ChangelogEntry, DeadEnd, Hypothesis, LabConfig } from './lab';

const REPO = 'ideoscopic/petrichor';
const REPO_URL = `https://github.com/${REPO}`;

// --- Types ---

export type FeedItemType =
	| 'experiment_completed'
	| 'experiment_started'
	| 'experiment_failed'
	| 'finding_added'
	| 'feedback_submitted'
	| 'changelog_event'
	| 'dead_end_recorded';

export interface FeedItem {
	id: string;
	date: string;
	type: FeedItemType;
	actor: { name: string; kind: 'agent' | 'human' };
	title: string;
	summary: string;
	badges: Array<{ label: string; class: string }>;
	actions: Array<{ label: string; url: string }>;
	detailLink: string | null;
	needsHuman: boolean;
}

// --- GitHub URL builders ---

export function experimentPRUrl(expId: string): string {
	const num = expId.replace(/[^0-9]/g, '');
	return `${REPO_URL}/pulls?q=head:experiment/${num}`;
}

export function validateFindingUrl(findingId: string): string {
	const filename = `feedback/validate-${findingId}.yaml`;
	const template = `from: "your-name"
date: "${new Date().toISOString().split('T')[0]}"
type: "validation"
regarding: "${findingId}"
comment: >
  [Your validation notes here]
actionable: true
suggested_action: "[Next steps]"`;
	return `${REPO_URL}/new/main?filename=${encodeURIComponent(filename)}&value=${encodeURIComponent(template)}`;
}

export function hypothesisFeedbackUrl(hypothesisId: string): string {
	const filename = `feedback/on-${hypothesisId}.yaml`;
	const template = `from: "your-name"
date: "${new Date().toISOString().split('T')[0]}"
type: "domain_expertise"
regarding: "${hypothesisId}"
comment: >
  [Your feedback here]
actionable: true
suggested_action: "[Suggested next steps]"`;
	return `${REPO_URL}/new/main?filename=${encodeURIComponent(filename)}&value=${encodeURIComponent(template)}`;
}

export function priorityChangeUrl(hypothesisId: string): string {
	const title = `Priority change: ${hypothesisId}`;
	const body = `## Requested Change

**Hypothesis:** ${hypothesisId}
**Current priority:** [fill in]
**Proposed priority:** [fill in]

## Rationale

[Why should this priority change?]`;
	return `${REPO_URL}/issues/new?title=${encodeURIComponent(title)}&body=${encodeURIComponent(body)}`;
}

export function changelogPRUrl(pr: string | null | undefined): string | null {
	if (!pr) return null;
	// If it's just a number, build the URL
	const num = String(pr).replace(/[^0-9]/g, '');
	if (num) return `${REPO_URL}/pull/${num}`;
	return null;
}

export function experimentFeedbackUrl(expId: string): string {
	const filename = `feedback/on-${expId}.yaml`;
	const template = `from: "your-name"
date: "${new Date().toISOString().split('T')[0]}"
type: "methodology_concern"
regarding: "${expId}"
comment: >
  [Your feedback on this experiment]
actionable: true
suggested_action: "[Suggested improvements]"`;
	return `${REPO_URL}/new/main?filename=${encodeURIComponent(filename)}&value=${encodeURIComponent(template)}`;
}

// --- Feed construction ---

function experimentToFeedItems(exp: Experiment): FeedItem[] {
	const items: FeedItem[] = [];
	const status = exp.status;
	if (!status) return items;

	const agent = status.agent ?? 'unknown';
	const needsReview = status.status === 'done' && !status.outcome;

	if (status.status === 'done' || status.status === 'completed') {
		items.push({
			id: `exp-${exp.id}`,
			date: status.completed ?? status.started ?? '1970-01-01',
			type: 'experiment_completed',
			actor: { name: agent, kind: 'agent' },
			title: `Experiment ${exp.id} completed`,
			summary: status.summary ?? 'No summary available.',
			badges: [
				{ label: status.status, class: 'done' },
				...(status.outcome ? [{ label: status.outcome, class: status.outcome }] : []),
			],
			actions: [
				{ label: 'Review PR', url: experimentPRUrl(exp.id) },
				{ label: 'Feedback', url: experimentFeedbackUrl(exp.id) },
			],
			detailLink: `/experiments/${exp.id}`,
			needsHuman: needsReview,
		});
	} else if (status.status === 'in_progress' || status.status === 'running') {
		items.push({
			id: `exp-${exp.id}`,
			date: status.started ?? '1970-01-01',
			type: 'experiment_started',
			actor: { name: agent, kind: 'agent' },
			title: `Experiment ${exp.id} in progress`,
			summary: status.summary ?? `Running workflow: ${status.workflow ?? 'unknown'}`,
			badges: [{ label: status.status, class: status.status }],
			actions: [
				{ label: 'View', url: experimentPRUrl(exp.id) },
			],
			detailLink: `/experiments/${exp.id}`,
			needsHuman: false,
		});
	} else if (status.status === 'failed') {
		items.push({
			id: `exp-${exp.id}`,
			date: status.completed ?? status.started ?? '1970-01-01',
			type: 'experiment_failed',
			actor: { name: agent, kind: 'agent' },
			title: `Experiment ${exp.id} failed`,
			summary: status.summary ?? 'Experiment failed.',
			badges: [{ label: 'failed', class: 'failed' }],
			actions: [
				{ label: 'Review PR', url: experimentPRUrl(exp.id) },
			],
			detailLink: `/experiments/${exp.id}`,
			needsHuman: true,
		});
	}

	return items;
}

function findingToFeedItem(f: Finding): FeedItem {
	const needsValidation = !!f.needs;
	return {
		id: `f-${f.id}`,
		date: f.date,
		type: 'finding_added',
		actor: { name: f.source ?? 'lab', kind: 'agent' },
		title: `Finding ${f.id} added`,
		summary: f.statement.trim().split('\n')[0],
		badges: [
			{ label: f.confidence, class: f.confidence },
			...(needsValidation ? [{ label: 'needs validation', class: 'needs-input' }] : []),
		],
		actions: needsValidation
			? [{ label: 'Validate', url: validateFindingUrl(f.id) }]
			: [],
		detailLink: '/knowledge',
		needsHuman: needsValidation,
	};
}

function feedbackToFeedItem(fb: Feedback, index: number): FeedItem {
	return {
		id: `fb-${index.toString().padStart(3, '0')}`,
		date: fb.date,
		type: 'feedback_submitted',
		actor: { name: fb.from, kind: 'human' },
		title: `Feedback from ${fb.from}`,
		summary: fb.comment.trim().split('\n')[0],
		badges: [{ label: fb.type.replace(/_/g, ' '), class: 'needs-input' }],
		actions: [],
		detailLink: null,
		needsHuman: false,
	};
}

function changelogToFeedItem(entry: ChangelogEntry): FeedItem {
	const isHuman = entry.proposed_by.startsWith('human');
	const prUrl = changelogPRUrl(entry.pr);
	return {
		id: `cl-${entry.id}`,
		date: entry.date,
		type: 'changelog_event',
		actor: { name: entry.proposed_by, kind: isHuman ? 'human' : 'agent' },
		title: entry.type === 'lab_initialized' ? 'Lab initialized' : `${entry.type.replace(/_/g, ' ')}: ${entry.target}`,
		summary: entry.rationale.trim().split('\n')[0],
		badges: [{ label: entry.type.replace(/_/g, ' '), class: 'pending' }],
		actions: prUrl ? [{ label: 'View PR', url: prUrl }] : [],
		detailLink: null,
		needsHuman: false,
	};
}

function deadEndToFeedItem(de: DeadEnd): FeedItem {
	return {
		id: `de-${de.id}`,
		date: de.date,
		type: 'dead_end_recorded',
		actor: { name: 'lab', kind: 'agent' },
		title: `Dead end: ${de.what}`,
		summary: de.lesson,
		badges: [{ label: 'dead end', class: 'failed' }],
		actions: [],
		detailLink: '/knowledge',
		needsHuman: false,
	};
}

export interface FeedStats {
	hypotheses: number;
	findings: number;
	experiments: number;
	deadEnds: number;
	needsHuman: number;
}

export function buildFeed(data: {
	experiments: Experiment[];
	findings: Finding[];
	feedback: Feedback[];
	changelog: ChangelogEntry[];
	dead_ends: DeadEnd[];
	hypotheses: Hypothesis[];
	config: LabConfig | null;
}): { items: FeedItem[]; stats: FeedStats } {
	const items: FeedItem[] = [];

	for (const exp of data.experiments) {
		items.push(...experimentToFeedItems(exp));
	}
	for (const f of data.findings) {
		items.push(findingToFeedItem(f));
	}
	for (const fb of data.feedback) {
		items.push(feedbackToFeedItem(fb, data.feedback.indexOf(fb)));
	}
	for (const entry of data.changelog) {
		items.push(changelogToFeedItem(entry));
	}
	for (const de of data.dead_ends) {
		items.push(deadEndToFeedItem(de));
	}

	// Sort by date descending
	items.sort((a, b) => b.date.localeCompare(a.date));

	const needsHumanCount = items.filter(i => i.needsHuman).length;

	// Also count hypotheses needing input (high priority + open)
	const hypothesesNeedingInput = data.hypotheses.filter(
		h => h.status === 'open' && h.priority === 'high'
	).length;

	const stats: FeedStats = {
		hypotheses: data.hypotheses.length,
		findings: data.findings.length,
		experiments: data.experiments.length,
		deadEnds: data.dead_ends.length,
		needsHuman: needsHumanCount + hypothesesNeedingInput,
	};

	return { items, stats };
}
