<script lang="ts">
	let { data } = $props();

	const statusOrder: Record<string, number> = { open: 0, testing: 1, supported: 2, refuted: 3 };
	const sorted = [...data.hypotheses].sort((a, b) => {
		const s = (statusOrder[a.status] ?? 9) - (statusOrder[b.status] ?? 9);
		if (s !== 0) return s;
		const pOrder: Record<string, number> = { high: 0, medium: 1, low: 2 };
		return (pOrder[a.priority ?? 'low'] ?? 9) - (pOrder[b.priority ?? 'low'] ?? 9);
	});
</script>

<svelte:head><title>Hypotheses</title></svelte:head>

<h1>Hypotheses</h1>
<p class="text-muted mb-1">{data.hypotheses.length} total &middot; {data.hypotheses.filter(h => h.status === 'open').length} open</p>

<div style="margin-top: 24px; display: flex; flex-direction: column; gap: 12px;">
	{#each sorted as hyp}
		<div class="card">
			<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
				<span class="mono" style="color: var(--accent); font-size: 15px;">{hyp.id}</span>
				<div style="display: flex; gap: 8px;">
					{#if hyp.priority}
						<span class="badge {hyp.priority}">{hyp.priority}</span>
					{/if}
					<span class="badge {hyp.status}">{hyp.status}</span>
				</div>
			</div>
			<p style="font-size: 15px; margin-bottom: 8px;">{hyp.statement}</p>
			{#if hyp.rationale}
				<p class="text-muted text-sm">{hyp.rationale}</p>
			{/if}
			{#if hyp.suggested_experiments?.length}
				<div class="mt-1">
					<span class="text-sm text-muted">Suggested experiments:</span>
					<ul style="margin-left: 20px; margin-top: 4px;">
						{#each hyp.suggested_experiments as exp}
							<li class="text-sm">{exp}</li>
						{/each}
					</ul>
				</div>
			{/if}
			{#if hyp.related_rq}
				<p class="text-sm text-muted mt-1">Related: {hyp.related_rq}</p>
			{/if}
		</div>
	{/each}
</div>
