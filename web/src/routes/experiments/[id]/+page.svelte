<script lang="ts">
	import { marked } from 'marked';
	let { data } = $props();
	const exp = data.experiment;
</script>

<svelte:head><title>{exp.id}</title></svelte:head>

<a href="/experiments" class="text-sm text-muted">&larr; All experiments</a>

<h1 style="margin-top: 12px;">{exp.id}</h1>

{#if exp.status}
	<div class="card mt-2">
		<h3>Status</h3>
		<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-top: 8px;">
			<div>
				<span class="text-sm text-muted">Status</span>
				<div><span class="badge {exp.status.status}">{exp.status.status}</span></div>
			</div>
			{#if exp.status.outcome}
				<div>
					<span class="text-sm text-muted">Outcome</span>
					<div><span class="badge {exp.status.outcome}">{exp.status.outcome}</span></div>
				</div>
			{/if}
			{#if exp.status.agent}
				<div>
					<span class="text-sm text-muted">Agent</span>
					<div class="mono text-sm">{exp.status.agent}</div>
				</div>
			{/if}
			{#if exp.status.workflow}
				<div>
					<span class="text-sm text-muted">Workflow</span>
					<div class="text-sm">{exp.status.workflow}</div>
				</div>
			{/if}
			{#if exp.status.hypothesis_ref}
				<div>
					<span class="text-sm text-muted">Hypothesis</span>
					<div class="mono text-sm">{exp.status.hypothesis_ref}</div>
				</div>
			{/if}
			{#if exp.status.started}
				<div>
					<span class="text-sm text-muted">Started</span>
					<div class="text-sm">{exp.status.started}</div>
				</div>
			{/if}
			{#if exp.status.completed}
				<div>
					<span class="text-sm text-muted">Completed</span>
					<div class="text-sm">{exp.status.completed}</div>
				</div>
			{/if}
		</div>
		{#if exp.status.summary}
			<p class="mt-1" style="font-size: 14px;">{exp.status.summary}</p>
		{/if}
	</div>
{/if}

{#if exp.hypothesis}
	<div class="card mt-2">
		<h3>Hypothesis</h3>
		<div class="text-sm">{@html marked(exp.hypothesis)}</div>
	</div>
{/if}

{#if exp.analysis}
	<div class="card mt-2">
		<h3>Analysis</h3>
		<div class="text-sm">{@html marked(exp.analysis)}</div>
	</div>
{/if}
