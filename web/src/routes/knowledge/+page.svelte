<script lang="ts">
	import { hypothesisFeedbackUrl, validateFindingUrl } from '$lib/feed';

	let { data } = $props();

	type TabType = 'hypotheses' | 'findings' | 'dead_ends';
	let activeTab = $state<TabType>('hypotheses');

	const statusOrder: Record<string, number> = { open: 0, testing: 1, supported: 2, refuted: 3 };
	const sortedHypotheses = $derived(
		[...data.hypotheses].sort((a, b) => {
			const s = (statusOrder[a.status] ?? 9) - (statusOrder[b.status] ?? 9);
			if (s !== 0) return s;
			const pOrder: Record<string, number> = { high: 0, medium: 1, low: 2 };
			return (pOrder[a.priority ?? 'low'] ?? 9) - (pOrder[b.priority ?? 'low'] ?? 9);
		})
	);

	const needsInputCount = $derived(data.hypotheses.filter((h: any) => h.status === 'open' && h.priority === 'high').length);
	const needsValidation = $derived(data.findings.filter((f: any) => !!f.needs).length);
</script>

<svelte:head><title>Knowledge</title></svelte:head>

<h1>Knowledge</h1>
<p class="text-muted mb-1">
	{data.hypotheses.length} hypotheses &middot; {data.findings.length} findings &middot; {data.dead_ends.length} dead ends
	{#if needsInputCount > 0}
		&middot; <span style="color: var(--orange);">{needsInputCount} need input</span>
	{/if}
	{#if needsValidation > 0}
		&middot; <span style="color: var(--orange);">{needsValidation} need validation</span>
	{/if}
</p>

<div class="knowledge-tabs">
	<button class:active={activeTab === 'hypotheses'} onclick={() => activeTab = 'hypotheses'}>
		Hypotheses ({data.hypotheses.length})
	</button>
	<button class:active={activeTab === 'findings'} onclick={() => activeTab = 'findings'}>
		Findings ({data.findings.length})
	</button>
	<button class:active={activeTab === 'dead_ends'} onclick={() => activeTab = 'dead_ends'}>
		Dead Ends ({data.dead_ends.length})
	</button>
</div>

{#if activeTab === 'hypotheses'}
	<div style="display: flex; flex-direction: column; gap: 12px;">
		{#each sortedHypotheses as hyp}
			<div class="card" class:needs-action={hyp.status === 'open' && hyp.priority === 'high'}>
				<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
					<span class="mono" style="color: var(--blue); font-size: 15px;">{hyp.id}</span>
					<div style="display: flex; gap: 6px;">
						{#if hyp.priority}
							<span class="badge {hyp.priority}">{hyp.priority}</span>
						{/if}
						<span class="badge {hyp.status}">{hyp.status}</span>
						{#if hyp.status === 'open' && hyp.priority === 'high'}
							<span class="badge needs-input">needs input</span>
						{/if}
					</div>
				</div>
				<p style="font-size: 15px; margin-bottom: 8px; color: var(--text-secondary);">{hyp.statement}</p>
				{#if hyp.rationale}
					<p class="text-muted text-sm">{hyp.rationale}</p>
				{/if}
				{#if hyp.suggested_experiments?.length}
					<div class="mt-1">
						<span class="text-sm text-muted">Suggested experiments:</span>
						<ul style="margin-left: 20px; margin-top: 4px;">
							{#each hyp.suggested_experiments as exp}
								<li class="text-sm" style="color: var(--text-secondary);">{exp}</li>
							{/each}
						</ul>
					</div>
				{/if}
				{#if hyp.related_rq}
					<p class="text-sm text-muted mt-1">Related: {hyp.related_rq}</p>
				{/if}
				<div class="mt-1 feed-actions">
					<a href={hypothesisFeedbackUrl(hyp.id)} target="_blank" rel="noopener noreferrer" class="feed-action-btn orange">
						Give Feedback
					</a>
				</div>
			</div>
		{/each}
	</div>
{:else if activeTab === 'findings'}
	<div style="display: flex; flex-direction: column; gap: 12px;">
		{#each data.findings as finding}
			<div class="card" class:needs-action={!!finding.needs}>
				<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
					<span class="mono" style="color: var(--teal); font-size: 15px;">{finding.id}</span>
					<div style="display: flex; gap: 6px; align-items: center;">
						<span class="text-sm text-muted">{finding.date}</span>
						<span class="badge {finding.confidence}">{finding.confidence}</span>
						{#if finding.needs}
							<span class="badge needs-input">needs validation</span>
						{/if}
					</div>
				</div>
				<p style="font-size: 15px; margin-bottom: 8px; color: var(--text-secondary);">{finding.statement}</p>
				{#if finding.source}
					<p class="text-sm text-muted">Source: {finding.source}</p>
				{/if}
				{#if finding.evidence?.length}
					<p class="text-sm text-muted">Evidence: {finding.evidence.join(', ')}</p>
				{/if}
				{#if finding.limitations}
					<p class="text-sm text-muted mt-1">Limitations: {finding.limitations}</p>
				{/if}
				{#if finding.needs}
					<p class="text-sm mt-1" style="color: var(--orange);">
						<span class="dot-human"></span> Needs: {finding.needs}
					</p>
					<div class="mt-1 feed-actions">
						<a href={validateFindingUrl(finding.id)} target="_blank" rel="noopener noreferrer" class="feed-action-btn orange">
							Validate
						</a>
					</div>
				{/if}
			</div>
		{/each}
	</div>
{:else if activeTab === 'dead_ends'}
	{#if data.dead_ends.length === 0}
		<div class="card empty">
			<p>No dead ends recorded yet.</p>
			<p class="text-sm text-muted">Dead ends appear when hypotheses are refuted or experiments fail to produce results.</p>
		</div>
	{:else}
		<div style="display: flex; flex-direction: column; gap: 12px;">
			{#each data.dead_ends as de}
				<div class="card" style="border-left: 3px solid var(--red);">
					<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
						<span class="mono" style="color: var(--red)">{de.id}</span>
						<span class="text-sm text-muted">{de.date}</span>
					</div>
					<p style="font-size: 14px; font-weight: 600; color: var(--text-secondary);">{de.what}</p>
					<p class="text-sm text-muted mt-1">Why it failed: {de.why_failed}</p>
					<p class="text-sm mt-1" style="color: var(--green);">Lesson: {de.lesson}</p>
				</div>
			{/each}
		</div>
	{/if}
{/if}
