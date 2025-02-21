<script>
	export let progress = 0; // Fraction out of 1
	export let name = 'None';
	export let barColor = '#FF0000';
</script>

<div class="barContainer" style="--theme-color: {barColor}; --progress: {progress}">
	<p>{name}</p>
	<div class="barBody">
		{#if progress != 0}
			<div class="barFill"></div>
		{/if}
		<div class="barBase"></div>
	</div>
</div>

<style>
	.barBody {
		width: 100px;
		display: flex;
		flex-direction: column;
		width: 250px;
		height: 25px;
	}

	.barContainer > p {
		margin: 0px;
		font-size: 20px;
		font-weight: 300;
		margin-top: 5px;
	}

	.barBase {
		background-color: #fafafa;
		border: 1px solid #c4c4c4;
		border-radius: 8px;
		height: 25px;
		position: absolute;
		width: 250px;
		margin-top: 4px;
	}

	.barFill {
		background-color: var(--theme-color);
		border: 1px solid var(--theme-color);
		border-radius: 8px;
		height: 25px;
		z-index: 1;
		position: absolute;
		width: calc(250px * var(--progress));
		margin-top: 4px;
	}

	.barContainer {
		display: flex;
		flex-direction: column;
	}
</style>
