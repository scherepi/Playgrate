<script lang="ts">
    import LogoCard from "$lib/LogoCard.svelte"
    import SpotifyBadge from "$lib/SpotifyBadge.svelte"
    import URLBox from "$lib/URLBox.svelte"
</script>
<style>
    #main-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 0;
        padding: 0;
        background-color: rgb(243, 209, 164);
        min-height: 100vh;
        width: 100vw;
        box-sizing: border-box;
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
</div>