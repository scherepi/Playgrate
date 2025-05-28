<!-- REMEMBER TO RUN NPM RUN BUILD WHEN YOU MAKE CHANGES TO THIS FILE. -->
<script>
	let rand = -1;

	function getRand() {
		fetch("./api/random")
		.then(d => d.text())
		.then(d => (rand = d));
	}

	function login() {
		fetch
	}
</script>

<style>
	h1 {
		color: #ff3e00;
	}
</style>

<LogoCard />

<h1>Random playlist: {rand}</h1>
<button on:click={getRand}>Get a random playlist name from me</button>

