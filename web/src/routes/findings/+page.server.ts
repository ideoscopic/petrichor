import { getFindings, getDeadEnds } from '$lib/lab';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		findings: getFindings(),
		dead_ends: getDeadEnds(),
	};
};
