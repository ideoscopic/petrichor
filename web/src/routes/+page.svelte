<script lang="ts">
	let { data } = $props();

	const openHypotheses = data.hypotheses.filter(h => h.status === 'open').length;
	const supportedHypotheses = data.hypotheses.filter(h => h.status === 'supported').length;
	const doneExperiments = data.experiments.filter(e => e.status?.status === 'done').length;
	const activeExperiments = data.experiments.filter(e =>
		e.status?.status === 'in_progress' || e.status?.status === 'running'
	).length;
</script>

<svelte:head>
	<title>{data.config?.name ?? 'Lab Dashboard'}</title>
</svelte:head>

<h1>{data.config?.name ?? 'Science Lab'}</h1>
<p class="text-muted" style="max-width: 720px; margin-bottom: 32px;">
	{data.config?.mission ?? ''}
</p>

<div class="section">
	<div class="stat-row">
		<div class="stat">
			<div class="number" style="color: var(--accent)">{data.hypotheses.length}</div>
			<div class="label">Hypotheses</div>
		</div>
		<div class="stat">
			<div class="number" style="color: var(--yellow)">{openHypotheses}</div>
			<div class="label">Open</div>
		</div>
		<div class="stat">
			<div class="number" style="color: var(--green)">{data.findings.length}</div>
			<div class="label">Findings</div>
		</div>
		<div class="stat">
			<div class="number" style="color: var(--purple)">{data.experiments.length}</div>
			<div class="label">Experiments</div>
		</div>
		<div class="stat">
			<div class="number" style="color: var(--orange)">{activeExperiments}</div>
			<div class="label">Active</div>
		</div>
		<div class="stat">
			<div class="number" style="color: var(--red)">{data.dead_ends.length}</div>
			<div class="label">Dead Ends</div>
		</div>
	</div>
</div>

{#if data.config?.research_questions?.length}
<div class="section">
	<h2>Research Questions</h2>
	<div class="grid-2">
		{#each data.config.research_questions as rq}
			<div class="card">
				<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
					<span class="mono" style="color: var(--accent)">{rq.id}</span>
					<span class="badge {rq.priority}">{rq.priority}</span>
				</div>
				<p style="font-size: 14px;">{rq.question}</p>
			</div>
		{/each}
	</div>
</div>
{/if}

<div class="section">
	<div class="section-header">
		<h2>Latest Findings</h2>
		<a href="/findings">View all</a>
	</div>
	{#if data.findings.length === 0}
		<div class="card empty">No findings yet</div>
	{:else}
		<div class="grid-2">
			{#each data.findings.slice(0, 4) as finding}
				<div class="card">
					<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
						<span class="mono" style="color: var(--green)">{finding.id}</span>
						<span class="badge {finding.confidence}">{finding.confidence}</span>
					</div>
					<p style="font-size: 14px;">{finding.statement}</p>
					{#if finding.needs}
						<p class="text-muted text-sm mt-1">Needs: {finding.needs}</p>
					{/if}
				</div>
			{/each}
		</div>
	{/if}
</div>

<div class="section">
	<div class="section-header">
		<h2>Open Hypotheses</h2>
		<a href="/hypotheses">View all</a>
	</div>
	{#if data.hypotheses.length === 0}
		<div class="card empty">No hypotheses yet</div>
	{:else}
		<div class="grid-2">
			{#each data.hypotheses.filter(h => h.status === 'open').slice(0, 4) as hyp}
				<div class="card">
					<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
						<span class="mono" style="color: var(--yellow)">{hyp.id}</span>
						<div>
							{#if hyp.priority}
								<span class="badge {hyp.priority}">{hyp.priority}</span>
							{/if}
						</div>
					</div>
					<p style="font-size: 14px;">{hyp.statement}</p>
					{#if hyp.related_rq}
						<p class="text-muted text-sm mt-1">Related: {hyp.related_rq}</p>
					{/if}
				</div>
			{/each}
		</div>
	{/if}
</div>

{#if data.changelog.length > 0}
<div class="section">
	<h2>Lab Changelog</h2>
	{#each data.changelog.slice(0, 5) as entry}
		<div class="card" style="margin-bottom: 8px;">
			<div style="display: flex; gap: 12px; align-items: center;">
				<span class="mono text-muted">{entry.date}</span>
				<span class="badge pending">{entry.type}</span>
				<span class="text-sm">{entry.rationale}</span>
			</div>
		</div>
	{/each}
</div>
{/if}
