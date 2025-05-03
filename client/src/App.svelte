<script>
	export let name;
	let rand = -1;

	function getRand() {
		fetch("./random")
		.then(d => d.text())
		.then(d => (rand = d));
	}
</script>

<h1>Random playlist: {rand}</h1>
<button on:click={getRand}>Get a random playlist name from me</button>