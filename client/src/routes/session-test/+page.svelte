<script lang="ts">
    let playlist_id = $state("placeholder")
    async function getPlaylistID() {
        const url = "/test-session"
        let response = await fetch(url)
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`)
        }
        playlist_id = await response.text()
    }
</script>
<h1>This will ideally have the current playlist_id listed below.</h1>
<button onclick={() => getPlaylistID()}>click to actualize</button>
<p>{playlist_id}</p>