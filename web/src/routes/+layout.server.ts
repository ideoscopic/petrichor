import { getLabConfig } from '$lib/lab';
import type { LayoutServerLoad } from './$types';

export const prerender = true;

export const load: LayoutServerLoad = async () => {
	const config = getLabConfig();
	return { labName: config?.name ?? 'Science Lab' };
};
