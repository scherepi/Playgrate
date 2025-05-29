<!-- REMEMBER TO RUN NPM RUN BUILD WHEN YOU MAKE CHANGES TO THIS FILE. -->
<script>
	import { LogoCard } from "./components/LogoCard.svelte"

	// Example code for executing a server-side function
	function getRand() {
		fetch("./api/random")
		.then(d => d.text())
		.then(d => (rand = d));
	}

	function login() {
		fetch("./spotify-login")
	}
</script>

<style>
</style>

<LogoCard />

<a href="/spotify-login">Log into Spotify:</a>

