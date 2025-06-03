<script lang="ts">
    import LogoCard from "$lib/LogoCard.svelte"
    import SpotifyBadge from "$lib/SpotifyBadge.svelte"
    import URLBox from "$lib/URLBox.svelte"
</script>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,200..900;1,200..900&display=swap');
    #main-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0;
        padding: 0;
        background-image: linear-gradient(0deg, rgb(243, 209, 164), rgb(126, 72, 21) 60%, rgb(243, 209, 164));
        min-height: 100vh;
        width: 100vw;
        box-sizing: border-box;
    }
    #request {
        margin-top: 25px;
        border-radius: 25px;
        border: 2px black solid;
        background-image: radial-gradient(rgb(66, 190, 190), lightblue)
    }
    h4 {
        font-family: 'Crimson Pro', serif;
        margin-left: 10px;
        margin-right: 10px;
    }
</style>
<SpotifyBadge --color="#26eb6b"/>
<div id="main-container">
    <LogoCard />
    <!--<a href="/spotify-login">Click here to log into Spotify</a>
    <a href="/start-scrape/apple-music/?playlistURL=https://music.apple.com/ca/playlist/scrobbleradio-mix/pl.u-dkelCypyBM">Test scrape</a>
    <a href="/view">Try to go to the view page</a> -->
    <br>
    <br>
    <URLBox />
    <div id="request">
        <h4>Please do not close the tab once started!</h4>
    </div>
</div>