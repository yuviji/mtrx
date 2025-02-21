<script>
	import { Chart, Card, A, Button, Dropdown, DropdownItem, Popover } from 'flowbite-svelte';

	export let companyData;
	export let categories;
	export let comp1Data;
	export let comp2Data;
	export let avgData;
	export let comp1Name;
	export let comp2Name;

	export let showComp;
	export let showAv;

	let series = [
		{
			name: 'You',
			type: 'area',
			data: companyData,
			color: '#95E398'
		}
	];

	if (showComp) {
		series.push({
			name: comp1Name,
			type: 'line',
			data: comp1Data,
			color: '#F3A0F7'
		});

		series.push({
			name: comp2Name,
			type: 'line',
			data: comp2Data,
			color: '#54bdff'
		});
	}

	if (showAv) {
		series.push({
			name: 'Comp Average',
			type: 'line',
			data: avgData,
			color: '#DCF086'
		});
	}

	let options = {
		chart: {
			height: '100%',
			type: 'area',
			fontFamily: 'Inter, sans-serif',
			dropShadow: {
				enabled: false
			},
			toolbar: {
				show: false
			}
		},
		tooltip: {
			enabled: true,
			x: {
				show: false
			},
			style: {
				fontFamily: 'Inter, sans-serif',
				fontSize: '20px',
				fontWeight: '300'
			},
			marker: {
				show: false
			}
		},
		fill: {
			type: ['gradient', 'fill', 'fill'],
			gradient: {
				opacityFrom: 0.55,
				opacityTo: 0,
				shade: '#1C64F2',
				gradientToColors: ['#D3FCD8']
			},
			solid: {
				opacity: [0.35, 1]
			}
		},
		dataLabels: {
			enabled: false
		},
		stroke: {
			width: 4,
			curve: 'straight'
		},
		grid: {
			show: true,
			strokeDashArray: 4,
			padding: {
				left: 20,
				right: 2,
				top: -20
			}
		},
		series: series,
		legend: {
			show: false
		},
		xaxis: {
			categories: categories,
			hideOverlappingLabels: true,
			rotate: 0,
			labels: {
				show: true,
				rotate: 0,
				style: {
					fontFamily: 'Inter, sans-serif',
					cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400',
					fontSize: '20px',
					fontWeight: '300'
				}
			},
			tooltip: {
				enabled: false
			},
			axisBorder: {
				show: false
			},
			axisTicks: {
				show: false
			}
		},
		yaxis: {
			show: false,
			labels: {
				style: {
					fontFamily: 'Inter, sans-serif',
					cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400',
					fontSize: '20px',
					fontWeight: '300'
				}
			}
		}
	};
</script>

<Chart {options} />

<style>
</style>
