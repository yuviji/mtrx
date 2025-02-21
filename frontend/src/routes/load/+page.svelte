<script>
	import { onMount } from 'svelte';
	import { auth, db } from '$lib/firebase.client';
	import * as firestore from 'firebase/firestore';
	import { goto } from '$app/navigation';
	import Spinner from './Spinner.svelte';
	import { loader } from './loader';
	import { writable } from 'svelte/store';

	onMount(async () => {
		if (!localStorage.getItem('uid')) {
			goto('/');
		}

		const uid = localStorage.getItem('uid');
		// @ts-ignore
		const docRef = firestore.doc(db, 'users', uid);
		const doc = await firestore.getDoc(docRef);
		if (doc.exists()) {
			const userdata = doc.data();
			// set(user, data);
			const yelp = userdata.yelp;
			const yelpTag = yelp.split('biz/').pop();
			fetch(
				`http://localhost:8088/https://green-sound-1619.ploomberapp.io/yelp/url=${yelpTag}`,
				{
					// method: 'POST',
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
				.then((response) => response.json())
				.then((data) => {
					// const bizDocRef = firestore.doc(db, 'businesses')
					// find the business in firebase by searching through 'businesses' for the one with the same name as data.business_name
					try {
						const bizDocRef = firestore.collection(db, 'businesses');
						const query = firestore.query(
							bizDocRef,
							firestore.where('business_name', '==', data.business_name)
						);
						const querySnapshot = firestore.getDocs(query).then((snapshot) => {
							snapshot.forEach((doc) => {
                                firestore.updateDoc(doc.ref, {
                                    business_name: userdata.displayName
                                });
                            });
						});

						// console.log(data);
						// set(user, data);
						goto('/dashboard');
					} catch (error) {
						console.error(error);
						auth.signOut();
						goto('/login');
					}
				});
		}
	});
</script>

<!-- write a svelte file with the following
- send a request to the server to scrape some data, wait until the data is returned and then goto('/dashboard')
- use the onMount function to send the request
- show a loading spinner while the request is being made, show some text as the request is being made
- in the script, also load firebase/firestore
-->

<div class="wrapper">
	<Spinner />
	<!-- <h1>Loading...</h1> -->
</div>

<style>
	.wrapper {
		min-height: 40rem;
		position: relative;
		background: rebeccapurple;
		padding: 1rem;
		color: white;
	}
</style>
