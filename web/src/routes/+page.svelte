<script lang="ts">
	import type { FeedItem } from '$lib/feed';

	let { data } = $props();

	type FilterType = 'all' | 'needs_me' | 'experiments' | 'findings' | 'changes';
	let activeFilter = $state<FilterType>('all');

	const needsHumanCount = $derived(data.feed.filter((i: FeedItem) => i.needsHuman).length);

	const filteredFeed = $derived.by(() => {
		const items: FeedItem[] = data.feed;
		switch (activeFilter) {
			case 'needs_me':
				return items.filter(i => i.needsHuman);
			case 'experiments':
				return items.filter(i =>
					i.type === 'experiment_completed' ||
					i.type === 'experiment_started' ||
					i.type === 'experiment_failed'
				);
			case 'findings':
				return items.filter(i =>
					i.type === 'finding_added' ||
					i.type === 'dead_end_recorded'
				);
			case 'changes':
				return items.filter(i =>
					i.type === 'changelog_event' ||
					i.type === 'feedback_submitted'
				);
			default:
				return items;
		}
	});

	function setFilter(f: FilterType) {
		activeFilter = f;
	}
</script>

<svelte:head>
	<title>{data.config?.name ?? 'Lab'} — Feed</title>
</svelte:head>

<!-- Compact Header -->
<div class="feed-header">
	<h1>{data.config?.name ?? 'Science Lab'}</h1>
	<div class="feed-meta">
		<span class="mission">{data.config?.mission?.split('\n')[0] ?? ''}</span>
	</div>
	<div class="feed-counts" style="margin-top: 8px;">
		<span>{data.stats.hypotheses} hyp</span>
		<span>&middot;</span>
		<span>{data.stats.findings} find</span>
		<span>&middot;</span>
		<span>{data.stats.experiments} exp</span>
		{#if data.stats.deadEnds > 0}
			<span>&middot;</span>
			<span>{data.stats.deadEnds} dead ends</span>
		{/if}
	</div>
</div>

<!-- Attention Banner -->
{#if data.stats.needsHuman > 0}
	<div class="attention-banner">
		<div class="attention-text">
			<span class="pulse-dot"></span>
			{data.stats.needsHuman} item{data.stats.needsHuman === 1 ? '' : 's'} need your attention
		</div>
		<button class="btn-show-me" onclick={() => setFilter('needs_me')}>Show me</button>
	</div>
{/if}

<!-- Filter Bar -->
<div class="filter-bar">
	<button class:active={activeFilter === 'all'} onclick={() => setFilter('all')}>All</button>
	<button
		class:active-orange={activeFilter === 'needs_me'}
		class:active={false}
		onclick={() => setFilter('needs_me')}
	>
		Needs Me{needsHumanCount > 0 ? ` (${needsHumanCount})` : ''}
	</button>
	<button class:active={activeFilter === 'experiments'} onclick={() => setFilter('experiments')}>Experiments</button>
	<button class:active={activeFilter === 'findings'} onclick={() => setFilter('findings')}>Findings</button>
	<button class:active={activeFilter === 'changes'} onclick={() => setFilter('changes')}>Changes</button>
</div>

<!-- Feed -->
<div class="feed-list">
	{#if filteredFeed.length === 0}
		<div class="card empty">
			<p>No items match this filter.</p>
		</div>
	{:else}
		{#each filteredFeed as item (item.id)}
			<div class="feed-item type-{item.type}" class:needs-human={item.needsHuman}>
				<div class="feed-item-header">
					<span class="feed-item-title">{item.title}</span>
					<div class="feed-item-badges">
						{#each item.badges as badge}
							<span class="badge {badge.class}">{badge.label}</span>
						{/each}
					</div>
				</div>
				<div class="feed-item-actor">
					{item.actor.name} &middot; {item.date}
				</div>
				<div class="feed-item-summary">{item.summary}</div>
				<div class="feed-item-footer">
					{#if item.actions.length > 0}
						<div class="feed-actions">
							{#each item.actions as action}
								<a
									href={action.url}
									target="_blank"
									rel="noopener noreferrer"
									class="feed-action-btn"
									class:orange={item.needsHuman}
								>
									{action.label}
								</a>
							{/each}
						</div>
					{/if}
					{#if item.detailLink}
						<a href={item.detailLink} class="detail-link">View details</a>
					{/if}
				</div>
			</div>
		{/each}
	{/if}
</div>
