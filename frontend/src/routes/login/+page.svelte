<script lang="ts">
	// login/+page.svelte
	import { session } from '$lib/session';
	import { auth, db } from '$lib/firebase.client';
	import * as firestore from 'firebase/firestore';
	import Logo from '../../icons/logo.svelte';
	import TopLeft from '../../icons/topLeft.svelte';
	import BottomRight from '../../icons/bottomRight.svelte';

	import {
		GoogleAuthProvider,
		signInWithPopup,
		signInWithEmailAndPassword,
		type UserCredential
	} from 'firebase/auth';
	import { goto } from '$app/navigation';

	let email: string = '';
	let password: string = '';

	async function loginWithMail() {
		await signInWithEmailAndPassword(auth, email, password)
			.then((result) => {
				const { user }: UserCredential = result;
				// load from firestore "users" collection

				if (user!.uid != null) {
					localStorage.setItem('uid', user?.uid);
					goto('/dashboard');
				}
			})
			.catch((error) => {
				return error;
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

<div class="login-container">
	<div class="login-form">
		<div class="logo">
			<Logo scale={0.38} />
		</div>
		<h1>Login</h1>
		<form on:submit={loginWithMail}>
			<input bind:value={email} type="text" placeholder="Email" />
			<input bind:value={password} type="password" placeholder="Password" />
			<button type="submit">Login</button>
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
