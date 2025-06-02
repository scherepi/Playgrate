<script lang="ts">
    import LogoCard from "$lib/LogoCard.svelte"
    import SpotifyBadge from "$lib/SpotifyBadge.svelte"
</script>
<style>
    #main-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0;
        padding: 0;
        background-color: tan;
        min-height: 100vh;
        width: 100vw;
        box-sizing: border-box;
    }
    .spotify-badge {
        position: absolute;
        left: 10px;
    }
</style>
<SpotifyBadge class:spotify-badge />
<div id="main-container">
    <LogoCard />

    <a href="/spotify-login">Click here to log into Spotify</a>
    <a href="/start-scrape/apple-music/?playlistURL=https://music.apple.com/ca/playlist/scrobbleradio-mix/pl.u-dkelCypyBM">Test scrape</a>
    <a href="/view">Try to go to the view page</a>
</div>