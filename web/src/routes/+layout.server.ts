import { getLabConfig, getHypotheses, getExperiments, getFindings } from '$lib/lab';
import type { LayoutServerLoad } from './$types';

export const prerender = true;

export const load: LayoutServerLoad = async () => {
	const config = getLabConfig();
	const hypotheses = getHypotheses();
	const experiments = getExperiments();
	const findings = getFindings();

	// Compute human action counts
	const hypothesesNeedingInput = hypotheses.filter(
		h => h.status === 'open' && h.priority === 'high'
	).length;
	const experimentsAwaitingReview = experiments.filter(
		e => e.status?.status === 'done' && !e.status?.outcome
	).length;
	const findingsNeedingValidation = findings.filter(f => !!f.needs).length;

	const totalActions = hypothesesNeedingInput + experimentsAwaitingReview + findingsNeedingValidation;

	return {
		labName: config?.name ?? 'Science Lab',
		humanActions: {
			total: totalActions,
			hypothesesNeedingInput,
			experimentsAwaitingReview,
			findingsNeedingValidation,
		},
	};
};
