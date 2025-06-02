<script>
    let url = '';
</script>

<style>
    @import url('');
    label {
        
    }
</style>

<label for="url-input">Enter URL:</label>
<input
    id="url-input"
    type="url"
    bind:value={url}
    placeholder="https://music.apple.com/your-playlist-id"
/>