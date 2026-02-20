import { getHypotheses, getFindings, getDeadEnds } from '$lib/lab';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		hypotheses: getHypotheses(),
		findings: getFindings(),
		dead_ends: getDeadEnds(),
	};
};
