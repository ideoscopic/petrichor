import { getExperiments } from '$lib/lab';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return { experiments: getExperiments() };
};
