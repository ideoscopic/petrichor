<script lang="ts">
	import '../app.css';
	import { page } from '$app/state';

	let { children } = $props();

	const navLinks = [
		{ href: '/', label: 'Dashboard' },
		{ href: '/hypotheses', label: 'Hypotheses' },
		{ href: '/experiments', label: 'Experiments' },
		{ href: '/findings', label: 'Findings' },
		{ href: '/workflows', label: 'Workflows' },
		{ href: '/feedback', label: 'Feedback' },
	];
</script>

<nav>
	<div class="inner">
		<span class="logo">Lab Dashboard</span>
		<div class="links">
			{#each navLinks as link}
				<a href={link.href} class:active={page.url.pathname === link.href}>
					{link.label}
				</a>
			{/each}
		</div>
	</div>
</nav>

<main class="container" style="padding-top: 32px; padding-bottom: 64px;">
	{@render children()}
</main>
