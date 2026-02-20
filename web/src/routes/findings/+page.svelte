<script lang="ts">
	let { data } = $props();
</script>

<svelte:head><title>Findings</title></svelte:head>

<h1>Findings</h1>
<p class="text-muted mb-1">{data.findings.length} findings &middot; {data.dead_ends.length} dead ends</p>

<div style="margin-top: 24px; display: flex; flex-direction: column; gap: 12px;">
	{#each data.findings as finding}
		<div class="card">
			<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
				<span class="mono" style="color: var(--green); font-size: 15px;">{finding.id}</span>
				<div style="display: flex; gap: 8px; align-items: center;">
					<span class="text-sm text-muted">{finding.date}</span>
					<span class="badge {finding.confidence}">{finding.confidence}</span>
				</div>
			</div>
			<p style="font-size: 15px; margin-bottom: 8px;">{finding.statement}</p>
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
				<p class="text-sm mt-1" style="color: var(--yellow);">Needs: {finding.needs}</p>
			{/if}
		</div>
	{/each}
</div>

{#if data.dead_ends.length > 0}
	<h2 style="margin-top: 40px;">Dead Ends</h2>
	<div style="margin-top: 16px; display: flex; flex-direction: column; gap: 12px;">
		{#each data.dead_ends as de}
			<div class="card" style="border-left: 3px solid var(--red);">
				<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
					<span class="mono" style="color: var(--red)">{de.id}</span>
					<span class="text-sm text-muted">{de.date}</span>
				</div>
				<p style="font-size: 14px; font-weight: 600;">{de.what}</p>
				<p class="text-sm text-muted mt-1">Why it failed: {de.why_failed}</p>
				<p class="text-sm mt-1" style="color: var(--green);">Lesson: {de.lesson}</p>
			</div>
		{/each}
	</div>
{/if}
