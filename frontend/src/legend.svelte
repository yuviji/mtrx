<script lang="ts">
	import { goto } from '$app/navigation';
	import { redirect } from '@sveltejs/kit';

	export let name = 'None';
	export let color = '#000000';
	export let route: string | null = null;

	let displayName = name;
	if (name.length > 17) {
		displayName = name.substring(0, 14) + '...';
	}
</script>

{#if route == null}
	<div class="legendContainer" style="--color: {color}">
		<div class="colorDot"></div>
		<p>{displayName}</p>
	</div>
{:else}
	<div class="legendContainer" style="--color: {color}">
		<div class="colorDot"></div>
		<a href={route} data-sveltekit-reload>{displayName}</a>
	</div>
{/if}

<style>
	.colorDot {
		width: 25px;
		height: 25px;
		border-radius: 12.5px;
		background-color: var(--color);
	}

	.legendContainer {
		display: flex;
		flex-direction: row;
		align-items: center;
	}

	.legendContainer > p {
		margin-top: 0px;
		margin-bottom: 0px;
		font-size: 23px;
		margin-left: 10px;
		font-weight: 300;
	}

	.legendContainer > a {
		margin-top: 0px;
		margin-bottom: 0px;
		text-decoration: none;
		margin-left: 10px;
		color: black;
		font-size: 23px;
		font-weight: 300;
	}
</style>
