<script>
	import DownArrow from './icons/downArrow.svelte';
	import UpArrow from './icons/upArrow.svelte';

	export let change = '';
	export let number = '';
	export let name = 'None';
	export let up = true;
	export let equal = false;
</script>

<div class="container">
	<p class="name">{name}</p>
	<div class="numbers">
		<div>
			<!-- svelte-ignore empty-block -->
			{#if equal}{:else if up}
				<UpArrow scale={0.86} />
			{:else}
				<DownArrow scale={0.86} />
			{/if}
		</div>
		<p class="bigNumber">{change}</p>
		<p class="smallNumber">{number}</p>
	</div>
</div>

<style>
	.container {
		display: flex;
		flex-direction: column;
	}

	p {
		margin: 0px;
	}

	.bigNumber {
		font-size: 50px;
		font-weight: 700;
		margin: 0px;
	}

	.smallNumber {
		font-size: 20px;
		font-weight: 600;
		margin: 0px;
		margin-bottom: 9px;
		margin-left: 10px;
		font-weight: 300;
	}

	.numbers > div {
		margin-bottom: 9px;
		margin-right: 5px;
	}

	.name {
		font-size: 20px;
		font-weight: 600;
		margin: 0px;
		font-weight: 300;
	}

	.numbers {
		display: flex;
		align-items: flex-end;
		flex-direction: row;
	}
</style>
