import { getFeedback, getHypotheses, getFindings } from '$lib/lab';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		feedback: getFeedback(),
		hypotheses: getHypotheses(),
		findings: getFindings(),
	};
};
