<script lang="ts">
	let { data } = $props();

	let name = $state('');
	let type = $state('domain_expertise');
	let regarding = $state('');
	let comment = $state('');
	let suggestedAction = $state('');
	let yamlOutput = $state('');

	const typeOptions = [
		{ value: 'domain_expertise', label: 'Domain Expertise' },
		{ value: 'priority_shift', label: 'Priority Change' },
		{ value: 'methodology_concern', label: 'Methodology Concern' },
		{ value: 'observation', label: 'General Observation' },
	];

	const referenceOptions = $derived([
		...data.hypotheses.map((h: any) => ({ value: h.id, label: `${h.id} — ${h.statement.slice(0, 60)}...` })),
		...data.findings.map((f: any) => ({ value: f.id, label: `${f.id} — ${f.statement.slice(0, 60)}...` })),
	]);

	function generateYaml() {
		if (!name.trim() || !comment.trim()) return;
		const today = new Date().toISOString().split('T')[0];
		let yaml = `from: "${name.trim()}"
date: "${today}"
type: "${type}"
regarding: ${regarding ? `"${regarding}"` : 'null'}
comment: >
  ${comment.trim().split('\n').join('\n  ')}
actionable: ${suggestedAction.trim() ? 'true' : 'false'}
suggested_action: ${suggestedAction.trim() ? `"${suggestedAction.trim()}"` : 'null'}`;
		yamlOutput = yaml;
	}

	let copied = $state(false);
	function copyYaml() {
		navigator.clipboard.writeText(yamlOutput);
		copied = true;
		setTimeout(() => copied = false, 2000);
	}
</script>

<svelte:head><title>Give Feedback</title></svelte:head>

<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
	<span class="dot-human" style="width: 10px; height: 10px;"></span>
	<h1 style="margin-bottom: 0;">Give Feedback</h1>
</div>
<p class="text-muted" style="margin-bottom: 32px; max-width: 640px;">
	Leave feedback for the lab's AI agents. Your input becomes part of the lab's
	shared state — agents read it during their observation phase.
</p>

<div style="max-width: 640px;">
	<p class="text-sm text-muted mb-1">
		Fill out the form to generate a feedback file. Copy the YAML and
		submit it as a PR to the <code>feedback/</code> directory.
	</p>
	<form onsubmit={(e) => { e.preventDefault(); generateYaml(); }}>
		<div class="form-group">
			<label for="name">Your name</label>
			<input id="name" type="text" bind:value={name} placeholder="Dr. Jane Smith" required />
		</div>
		<div class="form-group">
			<label for="type">Feedback type</label>
			<select id="type" bind:value={type}>
				{#each typeOptions as opt}
					<option value={opt.value}>{opt.label}</option>
				{/each}
			</select>
		</div>
		<div class="form-group">
			<label for="regarding">Regarding (optional)</label>
			<select id="regarding" bind:value={regarding}>
				<option value="">— General —</option>
				{#each referenceOptions as opt}
					<option value={opt.value}>{opt.label}</option>
				{/each}
			</select>
		</div>
		<div class="form-group">
			<label for="comment">Your feedback</label>
			<textarea
				id="comment"
				bind:value={comment}
				placeholder="Share your domain expertise, suggest priority changes, or flag methodological concerns..."
				rows="5"
				required
			></textarea>
		</div>
		<div class="form-group">
			<label for="action">Suggested action (optional)</label>
			<input
				id="action"
				type="text"
				bind:value={suggestedAction}
				placeholder="e.g. Add noise level as a covariate in moderator analysis"
			/>
		</div>
		<button type="submit" class="btn-action">Generate Feedback YAML</button>
	</form>

	{#if yamlOutput}
		<div class="card mt-2" style="border-left: 3px solid var(--orange); position: relative;">
			<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
				<span style="color: var(--orange); font-weight: 600; font-size: 14px;">
					Feedback ready
				</span>
				<button
					onclick={copyYaml}
					class="btn-secondary"
					style="padding: 4px 12px; font-size: 12px;"
				>
					{copied ? 'Copied!' : 'Copy'}
				</button>
			</div>
			<pre style="background: var(--bg); padding: 12px; border-radius: 6px; font-size: 13px; font-family: var(--font-mono); overflow-x: auto; white-space: pre-wrap;">{yamlOutput}</pre>
			<p class="text-sm text-muted mt-1">
				Save this as <code>feedback/NNN-your-name.yaml</code> and open a PR to the lab repo.
			</p>
		</div>
	{/if}
</div>
