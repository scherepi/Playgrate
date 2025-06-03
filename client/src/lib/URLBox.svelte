<script>
    let url = $state('');
    function submit() {
        // First step is to check if the user is signed in, we can do that quick, dirty, and local by checking the contents of the Login button
        const usernameElement = document.getElementById("username");
        if (usernameElement && usernameElement.innerHTML != "Login!") {
            // We're good to go! Let's build our redirect:
            let constructedURL = window.location['href']
            if (url !== '') {
                constructedURL = constructedURL + "/start-scrape/apple-music/?playlistURL=" + url;
                window.location.href = constructedURL;
            }
        }
    }
</script>

<style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:ital,wght@0,200..900;1,200..900&display=swap');
    input {
        font-family: 'Crimson Pro', serif;
        width: 50%;
        min-height: 10%;
        font-size: 30px;
        border-radius: 25px;
        padding-left: 10px;
        margin-right: 8px;
    }
    div {
        display: flex;
        justify-content: center;
        justify-items: center;
        width: 100%;
    }
    button {
        background-color: rgb(103, 218, 103);
        border-radius: 25px;
        font-size: 2em;
        font-family: 'Helvetica Neue', serif;
        color: #000;
    }
</style>
<div>
<input
    id="url-input"
    type="url"
    bind:value={url}
    placeholder="https://music.apple.com/your-playlist"
/>
<button onclick={submit}>Migrate!</button>
</div>