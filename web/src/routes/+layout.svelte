<script lang="ts">
	import '../app.css';
	import { page } from '$app/state';

	let { children, data } = $props();

	const navLinks = [
		{ href: '/', label: 'Feed', icon: '◫' },
		{ href: '/experiments', label: 'Experiments', icon: '⬡' },
		{ href: '/knowledge', label: 'Knowledge', icon: '◉' },
		{ href: '/feedback', label: 'Give Feedback', icon: '◈' },
	];

	const actions = $derived(data.humanActions);
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;0,8..60,700;1,8..60,400&display=swap" rel="stylesheet" />
</svelte:head>

<div class="app-layout">
	<aside class="sidebar">
		<div class="sidebar-header">
			<div class="lab-name">{data.labName}</div>
			<div class="lab-subtitle">Research Dashboard</div>
		</div>

		<nav class="sidebar-nav">
			{#each navLinks as link}
				<a href={link.href} class:active={
					link.href === '/'
						? page.url.pathname === '/'
						: page.url.pathname.startsWith(link.href)
				}>
					<span class="nav-icon">{link.icon}</span>
					{link.label}
				</a>
			{/each}
		</nav>

		{#if actions.total > 0}
			<div class="sidebar-actions">
				<div class="sidebar-actions-header">
					<span class="pulse-dot"></span>
					Your Actions
				</div>
				<div class="sidebar-actions-list">
					{#if actions.hypothesesNeedingInput > 0}
						<a href="/knowledge" class="sidebar-action-item">
							<span class="action-count">{actions.hypothesesNeedingInput}</span>
							hypothesis needs input
						</a>
					{/if}
					{#if actions.experimentsAwaitingReview > 0}
						<a href="/experiments" class="sidebar-action-item">
							<span class="action-count">{actions.experimentsAwaitingReview}</span>
							experiment awaiting review
						</a>
					{/if}
					{#if actions.findingsNeedingValidation > 0}
						<a href="/knowledge" class="sidebar-action-item">
							<span class="action-count">{actions.findingsNeedingValidation}</span>
							finding needs validation
						</a>
					{/if}
				</div>
			</div>
		{/if}
	</aside>

	<main class="main-content">
		{@render children()}
	</main>
</div>
