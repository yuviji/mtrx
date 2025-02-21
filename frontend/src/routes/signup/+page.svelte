<script lang="ts">
	// register/+page.svelte
	import { auth, db } from '$lib/firebase.client';
	import * as firestore from 'firebase/firestore';
	import { createUserWithEmailAndPassword } from 'firebase/auth';
	import { goto } from '$app/navigation';
	import { session } from '$lib/session';
	import Logo from '../../icons/logo.svelte';
	import TopLeft from '../../icons/topLeft.svelte';
	import BottomRight from '../../icons/bottomRight.svelte';


	let email: string = '';
	let password: string = '';
	let companyName: string = '';
	let yelp: string = '';
	let streetName: string = '';
	let city: string = '';
	let state: string = '';
	let zipCode: string = '';

	async function handleRegister() {
		await createUserWithEmailAndPassword(auth, email, password)
			.then((result) => {
				const { user } = result;

				const docRef = firestore.doc(db, 'users', user?.uid);
				firestore
					.setDoc(docRef, {
						displayName: companyName,
						email: email,
						location: {
							streetName: streetName,
							city: city,
							state: state,
							zipCode: zipCode
						},
						yelp: yelp
					})
					.then(() => {
						if (user!.uid != null) {
							localStorage.setItem('uid', user?.uid);
							const bizRef = firestore.collection(db, 'businesses');
							const query = firestore.query(bizRef, firestore.where('business_name', '==', companyName));
							const querySnapshot = firestore.getDocs(query).then((snapshot) => {
								if (snapshot.size === 0) {
									goto('/load')
								} else {
									goto('/dashboard');
								}
							});
						}
						goto('/');
					});
			})
			.catch((error) => {
				throw new Error(error);
			});
	}
</script>

<div class="background-containers">
	<div class="topleft-container">
		<TopLeft />
	  </div>
	  
	  <div class="bottomright-container">
		<BottomRight />
	  </div>
</div>

<!-- register/+page.svelte -->
<div class="login-container">
	<div class="login-form">
		<div class="logo">
			<Logo scale={0.38} />
		</div>
		<form on:submit={handleRegister}>
			<h2>Register</h2>
			<input bind:value={email} type="text" placeholder="Email" />
			<input bind:value={password} type="password" placeholder="Password" />
			<!-- make fields for company name, yelp, all required -->
			<input bind:value={companyName} type="text" placeholder="Company Name" required />
			<input bind:value={yelp} type="text" placeholder="Yelp" required />
			<!-- make required fields of street name, city, state, zip code -->
			<input bind:value={streetName} type="text" placeholder="Street Name" required />
			<input bind:value={city} type="text" placeholder="City" required />
			<input bind:value={state} type="text" placeholder="State" required />
			<input bind:value={zipCode} type="text" placeholder="Zip Code" required />
			<button type="submit">Register</button>
		</form>
	</div>
</div>

<style>
	@import '/src/styles.css';

	.login-container {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 100vh;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
			sans-serif;
		z-index: 1;
	}

	.logo {
		flex-direction: column;
		z-index: 2;
		align-items: center;
		justify-content: center;
		display: flex;
	}

	.login-form {
		background-color: #ffffff;
		padding: 2rem;
		border-radius: 0.5rem;
		border: 1px solid #c4c4c4;
		width: 100%;
		max-width: 300px;
		z-index: 1;
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

	h1 {
		color: #1f2937;
		font-size: 1.5rem;
		font-weight: 600;
		text-align: center;
		margin-bottom: 1.5rem;
	}

	form {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		align-items: center;
	}

	input {
		width: 92%;
		border: 1px solid #d1d5db;
		border-radius: 0.375rem;
		font-size: 1rem;
		color: #1f2937;
		padding: 10px;
		/* display: flex; */
		transition:
			border-color 0.15s ease-in-out,
			box-shadow 0.15s ease-in-out;
	}

	input:focus {
		outline: none;
		border-color: #95e398;
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
	}

	input::placeholder {
		color: #9ca3af;
	}

	button {
		background-color: #95e398;
		width: 100%;
		color: #ffffff;
		font-weight: 500;
		padding: 0.75rem 1rem;
		border: none;
		border-radius: 0.375rem;
		font-size: 1rem;
		cursor: pointer;
		transition: background-color 0.15s ease-in-out;
	}

	button:hover {
		background-color: #6fb772;
	}

	button:focus {
		outline: none;
		box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
	}
</style>
