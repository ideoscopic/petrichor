import { getExperiment, getExperiments } from '$lib/lab';
import { error } from '@sveltejs/kit';
import type { PageServerLoad, EntryGenerator } from './$types';

export const entries: EntryGenerator = () => {
	return getExperiments().map(e => ({ id: e.id }));
};

export const load: PageServerLoad = async ({ params }) => {
	const experiment = getExperiment(params.id);
	if (!experiment) throw error(404, 'Experiment not found');
	return { experiment };
};
