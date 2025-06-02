<script lang="ts">
    let username = $state("Login!")
    async function getSpotifyId() {
        const retrieval_url = "/spotify-id"
        let response = await fetch(retrieval_url)
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`)
        }
        username = await response.text()
        // If the username is "SESSIONNOTSET" in base64, we know the username is not set.
        if (username == "U0VTU0lPTk5PVFNFVA==") {
            // If this is someone's actual Spotify username, they can go fuck themselves.
            username = "Login!"
        }
    }
</script>
<style>
    div {
        display: flex;
        align-items: center;
        border-radius: 12% / 50%;

        width: 200px;
        height: 30px;
        border-radius: 50px;
        border: 1px solid black;

        padding: 1em 2em;
        background-color: var(--color, #fff);
        text-align: center;

        position: absolute;
        top: 3%;
        right: 10px;

        justify-content: center;
    }
    h2 {
        font-family: Arial, Helvetica, sans-serif;
        color: #0e1111;
    }
    a {
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 250%;
        height: 100%;
    }
</style>
<div>
    <a href="/spotify-login"><h2>{username}</h2></a>
</div>