<script lang="ts">
	let { data } = $props();
</script>

<svelte:head><title>Workflows</title></svelte:head>

<h1>Workflows</h1>
<p class="text-muted mb-1">{data.workflows.length} available workflows</p>

<div style="margin-top: 24px;" class="grid-2">
	{#each data.workflows as wf}
		<div class="card">
			<h3 style="color: var(--blue);">{wf.name}</h3>
			<p class="text-sm text-muted mb-1" style="font-family: var(--font-mono);">{wf.filename}</p>
			<p style="font-size: 14px; color: var(--text-secondary);">{wf.description}</p>
			{#if wf.steps}
				<div class="mt-1">
					<span class="text-sm text-muted">Steps:</span>
					<ol style="margin-left: 20px; margin-top: 4px;">
						{#each Object.entries(wf.steps) as [key, step]}
							<li class="text-sm" style="color: var(--text-secondary);">
								{typeof step === 'object' && step !== null && 'action' in step
									? (step as {action: string}).action
									: key}
							</li>
						{/each}
					</ol>
				</div>
			{/if}
		</div>
	{/each}
</div>
