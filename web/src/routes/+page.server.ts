import { getAllLabData } from '$lib/lab';
import { buildFeed } from '$lib/feed';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	const data = getAllLabData();
	const { items, stats } = buildFeed(data);

	return {
		feed: items,
		stats,
		config: data.config,
	};
};
