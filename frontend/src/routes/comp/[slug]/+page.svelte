<script lang="ts">
	import { page } from '$app/stores';
	import MiniGraph from '../../../miniGraph.svelte';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	import { session } from '$lib/session';
	import { auth, db } from '$lib/firebase.client';
	import * as firestore from 'firebase/firestore';

	import SvelteMarkdown from 'svelte-markdown';

	let slug_id = $page.params.slug;

	let updateToggle = true;

	function signout() {
		localStorage.clear();
		session.set({ loggedIn: false, user: null });
		goto('/');
	}

	function compback() {
		goto('/dashboard');
	}

	let yname = '';
	let cname = '';
	let categories1: String[] = [];
	let categories2: String[] = [];
	let ydata1: number[] = [];
	let cdata1: number[] = [];
	let ydata2: number[] = [];
	let cdata2: number[] = [];

	let llm_response = 'Generating response...';
	let llm_response2 = 'Generating response...';

	onMount(async () => {
		if (!localStorage.getItem('uid')) {
			goto('/');
		}

		// @ts-ignore
		const docRef = firestore.doc(db, 'users', localStorage.getItem('uid'));
		const docSnap = await firestore.getDoc(docRef);

		if (docSnap.exists()) {
			const companyData = docSnap.data();
			// find company in "businesses" collection with business_name == companyData.displayName
			const businessRef = firestore.collection(db, 'businesses');
			const businessQuery = firestore.query(
				businessRef,
				firestore.where('business_name', '==', companyData.displayName)
			);
			const businessSnap = await firestore.getDocs(businessQuery);
			const r1 = businessSnap.docs[0].data();

			// @ts-ignore
			const d2 = firestore.doc(db, 'businesses', slug_id);
			let a2 = await firestore.getDoc(d2);
			let r2 = a2.data();

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

			if (r1 != null && r2 != null) {
				yname = r1.business_name;
				cname = r2.business_name;
				for (let raw_category of raw_categories) {
					if (
						r1.moving_avg_rating[raw_category] != undefined &&
						r2.moving_avg_rating[raw_category] != undefined
					) {
						categories1.push(raw_category.substring(0, 3));

						ydata1.push(r1.moving_avg_rating[raw_category].toFixed(2));
						cdata1.push(r2.moving_avg_rating[raw_category].toFixed(2));

						if (categories1.length == 6) {
							break;
						}
					}
				}

				for (let raw_category of raw_categories) {
					if (
						r1.monthly_reviews_count[raw_category] != undefined &&
						r2.monthly_reviews_count[raw_category] != undefined
					) {
						categories2.push(raw_category.substring(0, 3));

						ydata2.push(r1.monthly_reviews_count[raw_category]);
						cdata2.push(r2.monthly_reviews_count[raw_category]);

						if (categories2.length == 6) {
							break;
						}
					}
				}
			}

			updateToggle = !updateToggle;

			let prompt =
				'I will provide some reviews for my small business, which you should take as an input and generate suggestions and ideas for how the establishment can be improved, action items that can enhance quality and customer satisifcation, and other improvement ideas you may have.' +
				'Dive right into the feedback. Do not give any introductions. You should separate ideas as new paragraphs and include a small title for the idea before describing it. Bold the title' +
				' IN YOUR RESPONSE, DO NOT MENTION THE REVIEW OR THE REVIEWER. ONLY MENTION THE INSIGHTS DERIVED ABOUT MY BUSINESS FROM THE CONTENT OF THE REVIEW. ' +
				'\n\nGiven this POSITIVE review of my business: \n' +
				r1.good_review[1] +
				'. And this NEGATIVE review of my business: \n' +
				r1.bad_review[1] +
				' come up with suggestions for my busness, do not mention the reviewer, do not describe the establishment, offer advice. After you generate the response, ensure that the word "reviewer" or any synonyms or substitutes for "reviewer" are not in your response. All in all, discuss ONLY my BUSINESS not the reviewer.';

			if (r2 != undefined) {
				let prompt2 =
					' IN YOUR RESPONSE, DO NOT MENTION THE REVIEW OR THE REVIEWER. ONLY MENTION THE INSIGHTS DERIVED ABOUT THE BUSINESS FROM THE CONTENT OF THE REVIEW. ' +
					'\n\nGiven this POSITIVE review: \n' +
					r2.good_review[1] +
					'. And this NEGATIVE review: \n' +
					r2.bad_review[1] +
					' Describe this competitor business.';

				fetch(
					`http://localhost:8088/https://green-sound-1619.ploomberapp.io/suggestions/prompt=${prompt2}`,
					{
						method: 'GET',
						mode: 'cors',
						headers: {
							'Content-Type': 'application/json'
						}
					}
				)
					.then((response) => {
						return response.text();
					})
					.then(async (data) => {
						llm_response2 = data;

						fetch(
							`http://localhost:8088/https://green-sound-1619.ploomberapp.io/suggestions/prompt=${prompt}`,
							{
								method: 'GET',
								mode: 'cors',
								headers: {
									'Content-Type': 'application/json'
								}
							}
						)
							.then((response) => {
								return response.text();
							})
							.then(async (data) => {
								llm_response = data;
							})
							.catch((error) => {
								console.log(error);
							});
					})
					.catch((error) => {
						console.log(error);
					});
			}
		}
	});
</script>

<div class="graphSidebar">
	<div class="dataBox">
		<h2>Review Averages</h2>
		<div class="graphContainer">
			{#key updateToggle}
				<MiniGraph cdata={cdata1} ydata={ydata1} categories={categories1} {cname} />
			{/key}
		</div>
	</div>
	<div class="dataBox">
		<h2>Review Counts</h2>
		<div class="graphContainer">
			{#key updateToggle}
				<MiniGraph cdata={cdata2} ydata={ydata2} categories={categories2} {cname} />
			{/key}
		</div>
	</div>
</div>

<div class="article">
	<div style="display:flex;flex-direction:row;justify-content:space-between;align-items: flex-end;">
		<h1>Direct Comparison</h1>
		<div style="display:flex;flex-direction:row;gap:20px;margin-bottom:10px">
			<button on:click={compback}>Dashboard</button>
			<button on:click={signout}>Sign Out</button>
		</div>
	</div>

	<div class="greyBox">
		<p>Here is a summary of your competitor {cname} based on their review data:</p>
	</div>

	{#key llm_response2}
		<SvelteMarkdown source={llm_response2} />
	{/key}

	<div class="greyBox">
		<p>Here is an AI-generated list of suggestions which you can use to improve your business.</p>
	</div>

	{#key llm_response}
		<SvelteMarkdown source={llm_response} />
	{/key}
</div>

<style>
	@import '/src/styles.css';

	:global(body) {
		margin: 0px;
		padding: 0px;
	}
	.graphContainer {
		height: 300px;
		margin: 20px;
	}

	.graphSidebar {
		width: 500px;
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow-x: hidden;
		position: fixed;
		top: 0;
		right: 0;
		z-index: 1;
		background-color: white;
		border-left: 1px solid #c4c4c4;
		margin-left: 50px;
	}

	:global(html) {
		scrollbar-width: none;
	} /* Firefox */
	:global(body) {
		-ms-overflow-style: none;
	} /* IE and Edge */
	:global(body)::-webkit-scrollbar,
	:global(body)::-webkit-scrollbar-button {
		display: none;
	}

	.article {
		width: calc(100vw - 650px);
		margin-left: 75px;
		margin-top: 100px;
		padding-bottom: 100px;
	}

	.dataBox > h2 {
		padding-left: 50px;
	}

	.graphSidebar {
		padding-top: 20px;
		padding-bottom: 20px;
		height: 100vh;
	}
	button {
		padding: 0;
		border: none;
		font-size: 23px;
		font-weight: 300;
		background: none;
	}

	* {
		font-size: 23px;
	}

	p {
		font-weight: 300;
	}

	.greyBox {
		padding-top: 20px;
		margin-top: 20px;
	}
</style>
