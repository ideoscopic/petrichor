<script lang="ts">
	let { data } = $props();
</script>

<svelte:head><title>Experiments</title></svelte:head>

<h1>Experiments</h1>
<p class="text-muted mb-1">{data.experiments.length} total</p>

{#if data.experiments.length === 0}
	<div class="card empty mt-2">
		<p>No experiments yet.</p>
		<p class="text-sm text-muted">Experiments appear here as agents create them in the <code>experiments/</code> directory.</p>
	</div>
{:else}
	<div style="margin-top: 24px; display: flex; flex-direction: column; gap: 12px;">
		{#each data.experiments as exp}
			<a href="/experiments/{exp.id}" class="card" style="text-decoration: none; color: inherit;">
				<div style="display: flex; justify-content: space-between; align-items: start;">
					<div>
						<span class="mono" style="color: var(--purple); font-size: 15px;">{exp.id}</span>
						{#if exp.status?.workflow}
							<span class="text-sm text-muted" style="margin-left: 12px;">{exp.status.workflow}</span>
						{/if}
					</div>
					<div style="display: flex; gap: 8px;">
						{#if exp.status?.outcome}
							<span class="badge {exp.status.outcome}">{exp.status.outcome}</span>
						{/if}
						<span class="badge {exp.status?.status ?? 'pending'}">{exp.status?.status ?? 'unknown'}</span>
					</div>
				</div>
				{#if exp.status?.summary}
					<p class="text-sm mt-1">{exp.status.summary}</p>
				{/if}
				{#if exp.status?.agent}
					<p class="text-sm text-muted mt-1">Agent: {exp.status.agent}</p>
				{/if}
			</a>
		{/each}
	</div>
{/if}
