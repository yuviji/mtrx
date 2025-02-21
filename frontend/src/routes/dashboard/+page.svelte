<script lang="ts">
	import Checkbox from '../../checkbox.svelte';
	import Graph from '../../graph.svelte';
	import Legend from '../../legend.svelte';
	import Metric from '../../metric.svelte';
	import ProgressBar from '../../progressBar.svelte';
	import Info from '../../icons/info.svelte';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	// firebase, firestore imports

	import { session } from '$lib/session';
	import { auth, db } from '$lib/firebase.client';
	import * as firestore from 'firebase/firestore';

	/**
	 * @type {firestore.DocumentData | null}
	 */
	let companyData = null;
	import TopLeft from '../../icons/topLeft.svelte';
	import BottomRight from '../../icons/bottomRight.svelte';
	import { documentId } from 'firebase/firestore/lite';

	let categories: String[] = [];
	let ydata: number[] = [];
	let cdata1: number[] = [];
	let cdata2: number[] = [];
	let avgdata: number[] = [];
	let c1name = 'Company A';
	let c2name = 'Company B';
	let yname = 'Loading...';

	let competitorIds: number[] = [0, 0];
	let nps = 0;
	let npsChange = 0;

	let reviewCount = 0;
	let reviewChange = 0;

	let foodSentiment = 0;
	let environmentSentiment = 0;
	let serviceSentiment = 0;

	let updateToggle = true;

	let hideComp = false;
	let hideAv = false;

	onMount(async () => {
		if (!localStorage.getItem('uid')) {
			goto('/');
		}

		// @ts-ignore
		const docRef = firestore.doc(db, 'users', localStorage.getItem('uid'));
		const docSnap = await firestore.getDoc(docRef);

		if (docSnap.exists()) {
			companyData = docSnap.data();
			// find company in "businesses" collection with business_name == companyData.displayName
			const businessRef = firestore.collection(db, 'businesses');
			const businessQuery = firestore.query(
				businessRef,
				firestore.where('business_name', '==', companyData.displayName)
			);
			const businessSnap = await firestore.getDocs(businessQuery);
			const maindata = businessSnap.docs[0].data();

			yname = maindata.business_name;

			foodSentiment = (maindata.business_topics['food'] + 1) / 2;
			environmentSentiment = (maindata.business_topics['environment'] + 1) / 2;
			serviceSentiment = (maindata.business_topics['service'] + 1) / 2;

			let raw_categories = [
				'Sep 2023',
				'Oct 2023',
				'Nov 2023',
				'Dec 2023',
				'Jan 2024',
				'Feb 2024',
				'Mar 2024',
				'Apr 2024',
				'May 2024',
				'Jun 2024',
				'Jul 2024',
				'Aug 2024'
			].reverse();

			let npsSet = false;
			let lastNps = 0.0;

			let countSet = false;
			let lastCount = 0;

			for (var category of raw_categories) {
				if (maindata.monthly_nps[category] != null) {
					if (!npsSet) {
						nps = maindata.monthly_nps[category];
						npsSet = true;
					} else {
						lastNps = maindata.monthly_nps[category];
						break;
					}

					if (!countSet) {
						reviewCount = maindata.monthly_reviews_count[category];
						countSet = true;
					} else {
						lastCount = maindata.monthly_reviews_count[category];
						break;
					}
				}
			}

			npsChange = nps - lastNps;

			reviewChange = reviewCount - lastCount;

			// fetch request to https://green-sound-1619.ploomberapp.io/db/competitors/business_id={businessData.id}
			fetch(
				`http://localhost:8088/https://green-sound-1619.ploomberapp.io/db/competitors/business_id=${businessSnap.docs[0].id}`,
				{
					method: 'GET',
					mode: 'cors',
					headers: {
						'Content-Type': 'application/json'
						// 'Access-Control-Allow-Origin': 'http://localhost:5173',
						// 'Access-Control-Allow-Credentials': 'true',
						// 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
						// 'Access-Control-Allow-Headers': 'Content-Type, Origin, Accept'
					}
				}
			)
				.then((response) => {
					return response.json();
				})
				.then(async (data) => {
					competitorIds = data;

					// @ts-ignore
					const d1 = firestore.doc(db, 'businesses', competitorIds[0]);
					let a1 = await firestore.getDoc(d1);
					let r1 = a1.data();

					// @ts-ignore
					const d2 = firestore.doc(db, 'businesses', competitorIds[1]);
					let a2 = await firestore.getDoc(d2);
					let r2 = a2.data();

					if (r1 != null && r2 != null) {
						c1name = r1.business_name;
						c2name = r2.business_name;
						for (let raw_category of raw_categories) {
							if (
								maindata.moving_avg_rating[raw_category] != undefined &&
								r1.moving_avg_rating[raw_category] != undefined &&
								r2.moving_avg_rating[raw_category] != undefined
							) {
								categories.push(raw_category.substring(0, 3));
								ydata.push(maindata.moving_avg_rating[raw_category].toFixed(2));
								cdata1.push(r1.moving_avg_rating[raw_category].toFixed(2));
								cdata2.push(r2.moving_avg_rating[raw_category].toFixed(2));

								let avg: number =
									(r1.moving_avg_rating[raw_category] + r2.moving_avg_rating[raw_category]) / 2;
								avgdata.push(Math.round(avg * 100) / 100);
								if (categories.length == 6) {
									break;
								}
							}
						}
					}

					updateToggle = !updateToggle;
				})
				.catch((error) => {});
		}
	});
	function signout() {
		localStorage.clear();
		session.set({ loggedIn: false, user: null });
		goto('/');
	}

	// load
</script>

<div class="background-containers">
	<div class="topleft-container">
		<TopLeft />
	</div>

	<div class="bottomright-container">
		<BottomRight />
	</div>
</div>

<div class="dashboardContainer">
	<div class="dashboardLeft">
		<div class="dashboardTitle">
			<h1>Dashboard</h1>

			<p>{yname == 'Loading...' ? yname : yname + ' - Average Review Ratings'}</p>
		</div>

		<div class="graphContainer">
			{#key [updateToggle, hideAv, hideComp]}
				<Graph
					companyData={ydata}
					{categories}
					comp1Data={cdata1}
					comp1Name={c1name}
					comp2Data={cdata2}
					comp2Name={c2name}
					avgData={avgdata}
					showAv={!hideAv}
					showComp={!hideComp}
				/>
			{/key}
		</div>
	</div>

	<div class="dashboardRight">
		<div>
			<div class="right-top" style="display:flex;flex-direction:row;justify-content:space-between">
				<h2>Key Metrics</h2>
				<button on:click={signout} style="font-size: 23px;">Sign Out</button>
			</div>
			<div class="greyBox" style="display:flex;flex-direction:row;justify-content:space-between;">
				<Metric
					change={npsChange.toFixed(2)}
					number={nps.toFixed(2)}
					name="NPS"
					up={npsChange >= 0}
					equal={npsChange == 0}
				/>
				<Metric
					change={reviewChange.toString()}
					number={reviewCount.toString() + ' per month'}
					name="Review Count"
					up={reviewChange >= 0}
					equal={reviewChange == 0}
				/>
			</div>
		</div>
		<div class="middleSection">
			<div class="middleLeft">
				<p>Click on a company in the legend to start an in-depth comparison</p>
				<div class="checkboxes">
					<div class="check">
						<label class="container">
							<input type="checkbox" bind:checked={hideComp} />
							<span class="checkmark"></span>
						</label>
						<!-- <Checkbox bind:checked={hideComp} /> -->
						<p>Hide Competition</p>
					</div>
					<div class="check">
						<label class="container">
							<input type="checkbox" bind:checked={hideAv} />
							<span class="checkmark"></span>
						</label>
						<p>Hide Average</p>
					</div>
				</div>
			</div>
			<div class="middleRight">
				<p>Customer opinions on:</p>
				<ProgressBar progress={foodSentiment} barColor="#95E398" name="Food" />
				<ProgressBar progress={environmentSentiment} barColor="#F3A0F7" name="Environment" />
				<ProgressBar progress={serviceSentiment} barColor="#54bdff" name="Service" />
			</div>
		</div>
		<div>
			<h2>Legend</h2>
			<div class="legendBottom">
				<div>
					<Legend color="#95E398" name="You" />
					<Legend color="#DCF086" name="Comp Average" />
				</div>
				<div>
					{#key updateToggle}
						<Legend color="#F3A0F7" name={c1name} route="/comp/{competitorIds[0]}" />
						<Legend color="#54bdff" name={c2name} route="/comp/{competitorIds[1]}" />
					{/key}
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	@import '/src/styles.css';

	.dashboardContainer {
		display: flex;
		flex-direction: row;
		width: 100vw;
		height: 100vh;
		z-index: 1;
	}

	.dashboardLeft {
		flex-grow: 1;
		padding: 55px;
		display: flex;
		flex-direction: column;
		z-index: 1;
	}

	.dashboardRight {
		width: 600px;
		padding: 55px;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		margin-bottom: 30px;
		z-index: 1;
	}

	.check {
		display: flex;
		flex-direction: row;
	}

	.graphContainer {
		width: 100%;
		height: calc(100vh - 30px);
		margin-top: 20px;
	}

	.dashboardTitle {
		margin-bottom: 30px;
	}

	:global(body) {
		height: 100%;
		overflow-y: hidden;
		margin: 0px;
		padding: 0px;
		width: 100vw;
		height: 100vh;
	}

	.background-containers {
		position: fixed;
		top: 0;
		left: 0;
		width: 100vw;
		height: 100vh;
		pointer-events: none;
		z-index: 0;
	}

	.topleft-container {
		position: absolute;
		top: -200px;
		left: -170px;
	}

	.bottomright-container {
		position: absolute;
		bottom: -300px;
		right: -50px;
	}

	.middleSection {
		display: flex;
		flex-direction: row;
	}

	.middleLeft {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

	.middleRight {
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		height: 220px;
		margin-left: 10px;
	}

	.checkboxes > .check {
		margin-top: 15px;
	}

	.legendBottom {
		display: flex;
		flex-direction: row;
	}

	.legendBottom > div {
		margin-right: 70px;
		display: flex;
		flex-direction: column;
		height: 70px;
		justify-content: space-between;
	}

	button {
		padding: 0;
		border: none;
		font-size: 23px;
		font-weight: 300;
		background: none;
	}
	.container {
		display: block;
		position: relative;
		padding-left: 35px;
		margin-bottom: 12px;
		cursor: pointer;
		font-size: 22px;
		-webkit-user-select: none;
		-moz-user-select: none;
		-ms-user-select: none;
		user-select: none;
	}

	/* Hide the browser's default checkbox */
	.container input {
		position: absolute;
		opacity: 0;
		cursor: pointer;
		height: 0;
		width: 0;
	}

	/* Create a custom checkbox */
	.checkmark {
		position: absolute;
		top: 0;
		left: 0;
		height: 25px;
		width: 25px;
		background-color: #fafafa;
		border: 1px solid #c4c4c4;
		border-radius: 5px;
		border: 2p;
	}

	/* On mouse-over, add a grey background color */
	.container:hover input ~ .checkmark {
		background-color: #ccc;
	}

	/* When the checkbox is checked, add a blue background */
	.container input:checked ~ .checkmark {
		background-color: #54bdff;
		border: 1px solid #54bdff;
	}

	/* Create the checkmark/indicator (hidden when not checked) */
	.checkmark:after {
		content: '';
		position: absolute;
		display: none;
	}

	/* Show the checkmark when checked */
	.container input:checked ~ .checkmark:after {
		display: block;
	}

	/* Style the checkmark/indicator */
	.container .checkmark:after {
		left: 9px;
		top: 5px;
		width: 5px;
		height: 10px;
		border: solid white;
		border-width: 0 3px 3px 0;
		-webkit-transform: rotate(45deg);
		-ms-transform: rotate(45deg);
		transform: rotate(45deg);
	}
</style>
