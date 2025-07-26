<script lang="ts">
    import { onMount } from 'svelte';
    
    let scraped_playlist_id = "";
    
    async function getScrapeID() {
        console.log("Retrieving playlist id")
        const retrieval_url = "/scraped-playlist-id";
        let response = await fetch(retrieval_url);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`)
        }
        scraped_playlist_id = await response.text()
        console.log("Got playlist id " + scraped_playlist_id)
        // If they got this far, we don't need to check that the id is valid.
    }
    
    let threadFinished = false;

    async function checkForThread() {
        console.log("checking for thread")
        const retrieval_url = "/check-thread/"
        let response = await fetch(retrieval_url + scraped_playlist_id)
        let response_text = await response.text()
        let status = JSON.parse(response_text)["response"];
        console.log("Response: " + response_text)
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }
        if (status == "Done") {
            threadFinished = true;
        }
    }

    setInterval(async () => {
        // We're gonna continually check for whether the playlist is done scraping.
        await checkForThread();
        if (threadFinished) {
            window.location.href = "/generateAM"
        }
    }, 2400)
    
    // Surely there's a better way to animate this, but I don't really care right now.
    let message = $state("Loading.");

    setInterval(() => {
        switch (message) {
            case "Loading.":
                message = "Loading..";
                break;
            case "Loading..":
                message = "Loading..."
                break;
            case "Loading...":
                message = "Loading."
                break;
        }
    }, 800)

    onMount(async () => {
        getScrapeID()
    })
</script>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,200..900;1,200..900&display=swap');
    div {
        margin: 0px;
        padding: 0px;
        min-height: 100vh;
        width: 100vw;
        box-sizing: border-box;
        height: auto;
        width: auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        justify-items: center;
        align-items: center;
        background-color: rgb(243, 209, 164);
    }
    h1 {
        font-family: 'Crimson Pro', serif;
        color: #2a0134;
        font-size: 100px;
        margin-bottom: 10px;
    }
    p {
        font-family: 'Crimson Pro', serif;
        color: #3f024f;
        font-size: 40px;
        margin-top: 10px;
    }
</style>
<div>
    <h1>{message}</h1>
    <p>Please don't close out of the tab!</p>
</div>