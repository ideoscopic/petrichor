<script lang="ts">
	let { data } = $props();

	const openHypotheses = data.hypotheses.filter(h => h.status === 'open').length;
	const highPriorityOpen = data.hypotheses.filter(h => h.status === 'open' && h.priority === 'high').length;
	const activeExperiments = data.experiments.filter(e =>
		e.status?.status === 'in_progress' || e.status?.status === 'running'
	).length;
	const experimentsAwaitingReview = data.experiments.filter(
		e => e.status?.status === 'done' && !e.status?.outcome
	).length;
	const findingsNeedingValidation = data.findings.filter(f => !!f.needs).length;

	const totalActions = highPriorityOpen + experimentsAwaitingReview + findingsNeedingValidation;

	function isHumanActivity(entry: { type: string; proposed_by: string }): boolean {
		const humanTypes = ['feedback', 'priority_shift', 'methodology_concern'];
		return humanTypes.includes(entry.type) || entry.proposed_by === 'human';
	}
</script>

<svelte:head>
	<title>{data.config?.name ?? 'Lab Dashboard'}</title>
</svelte:head>

<h1>{data.config?.name ?? 'Science Lab'}</h1>
<p class="text-muted" style="max-width: 720px; margin-bottom: 28px;">
	{data.config?.mission ?? ''}
</p>

<!-- Human Actions Banner -->
{#if totalActions > 0}
	<div class="actions-banner">
		<div class="actions-banner-header">
			<span class="pulse-dot"></span>
			Actions Needed
		</div>
		<div class="actions-banner-items">
			{#if highPriorityOpen > 0}
				<a href="/hypotheses" class="action-chip">
					<span class="chip-count">{highPriorityOpen}</span>
					high-priority hypotheses need input
				</a>
			{/if}
			{#if experimentsAwaitingReview > 0}
				<a href="/experiments" class="action-chip">
					<span class="chip-count">{experimentsAwaitingReview}</span>
					experiments awaiting review
				</a>
			{/if}
			{#if findingsNeedingValidation > 0}
				<a href="/findings" class="action-chip">
					<span class="chip-count">{findingsNeedingValidation}</span>
					findings need validation
				</a>
			{/if}
		</div>
	</div>
{/if}

<!-- Stats -->
<div class="section">
	<div class="stat-row">
		<div class="stat">
			<div class="label">Hypotheses</div>
			<div class="number" style="color: var(--blue)">{data.hypotheses.length}</div>
		</div>
		<div class="stat">
			<div class="label">Open</div>
			<div class="number" style="color: var(--amber)">{openHypotheses}</div>
		</div>
		<div class="stat">
			<div class="label">Findings</div>
			<div class="number" style="color: var(--teal)">{data.findings.length}</div>
		</div>
		<div class="stat">
			<div class="label">Experiments</div>
			<div class="number" style="color: var(--purple)">{data.experiments.length}</div>
		</div>
		<div class="stat">
			<div class="label">Active</div>
			<div class="number" style="color: var(--amber)">{activeExperiments}</div>
		</div>
		<div class="stat">
			<div class="label">Dead Ends</div>
			<div class="number" style="color: var(--red)">{data.dead_ends.length}</div>
		</div>
	</div>
</div>

<!-- Two-column grid: Research Questions + Latest Findings -->
<div class="grid-2" style="margin-bottom: 36px; align-items: start;">
	<!-- Research Questions -->
	{#if data.config?.research_questions?.length}
		<div>
			<div class="section-label">Research Questions</div>
			<div style="display: flex; flex-direction: column; gap: 10px;">
				{#each data.config.research_questions as rq}
					<div class="card">
						<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 6px;">
							<span class="mono" style="color: var(--blue)">{rq.id}</span>
							<span class="badge {rq.priority}">{rq.priority}</span>
						</div>
						<p style="font-size: 14px; color: var(--text-secondary);">{rq.question}</p>
					</div>
				{/each}
			</div>
		</div>
	{/if}

	<!-- Latest Findings -->
	<div>
		<div class="section-header" style="margin-bottom: 14px;">
			<span class="section-label" style="margin-bottom: 0;">Latest Findings</span>
			<a href="/findings" class="text-sm">View all</a>
		</div>
		{#if data.findings.length === 0}
			<div class="card empty">No findings yet</div>
		{:else}
			<div style="display: flex; flex-direction: column; gap: 10px;">
				{#each data.findings.slice(0, 4) as finding}
					<div class="card" class:needs-action={!!finding.needs}>
						<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 6px;">
							<span class="mono" style="color: var(--teal)">{finding.id}</span>
							<span class="badge {finding.confidence}">{finding.confidence}</span>
						</div>
						<p style="font-size: 14px; color: var(--text-secondary);">{finding.statement}</p>
						{#if finding.needs}
							<p class="text-sm mt-1" style="color: var(--orange);">
								<span class="dot-human"></span> Needs: {finding.needs}
							</p>
						{/if}
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div>

<!-- Open Hypotheses -->
<div class="section">
	<div class="section-header">
		<span class="section-label" style="margin-bottom: 0;">Open Hypotheses</span>
		<a href="/hypotheses" class="text-sm">View all</a>
	</div>
	{#if data.hypotheses.length === 0}
		<div class="card empty">No hypotheses yet</div>
	{:else}
		<div class="grid-2">
			{#each data.hypotheses.filter(h => h.status === 'open').slice(0, 4) as hyp}
				<div class="card" class:needs-action={hyp.priority === 'high'}>
					<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 6px;">
						<span class="mono" style="color: var(--blue)">{hyp.id}</span>
						<div style="display: flex; gap: 6px;">
							{#if hyp.priority}
								<span class="badge {hyp.priority}">{hyp.priority}</span>
							{/if}
							{#if hyp.priority === 'high'}
								<span class="badge needs-input">needs input</span>
							{/if}
						</div>
					</div>
					<p style="font-size: 14px; color: var(--text-secondary);">{hyp.statement}</p>
					{#if hyp.related_rq}
						<p class="text-muted text-sm mt-1">Related: {hyp.related_rq}</p>
					{/if}
				</div>
			{/each}
		</div>
	{/if}
</div>

<!-- Lab Changelog (Timeline) -->
{#if data.changelog.length > 0}
	<div class="section">
		<div class="section-label">Lab Changelog</div>
		<div class="timeline">
			{#each data.changelog.slice(0, 8) as entry}
				<div class="timeline-entry">
					<div class="timeline-dot" class:human={isHumanActivity(entry)} class:agent={!isHumanActivity(entry)}></div>
					<div class="timeline-content">
						<div class="timeline-meta">
							<span class="timeline-date">{entry.date}</span>
							<span class="badge {entry.type === 'feedback' ? 'needs-input' : 'pending'}">{entry.type}</span>
						</div>
						<p class="timeline-text">{entry.rationale}</p>
					</div>
				</div>
			{/each}
		</div>
	</div>
{/if}
