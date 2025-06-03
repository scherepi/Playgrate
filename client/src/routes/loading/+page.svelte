<script lang="ts">
    let message = $state("Loading.");
    // Surely there's a better way to animate this, but I don't really care right now.
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
        font-size: 18px;
        margin-top: 10px;
        font-family: 'Crimson Pro', serif;
    }
</style>
<div>
    <h1>{message}</h1>
</div>