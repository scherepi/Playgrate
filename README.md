![Logo card](https://hc-cdn.hel1.your-objectstorage.com/s/v3/5b72e6ea8969529d43298cbf3285a64548ce4409_image.png)
# PLAYGRATE: *IT SHOULDN'T BE SO DAMN HARD*.
![Hackatime embed](https://hackatime-badge.hackclub.com/U083W5CCFDG/Playgrate)

<h6><strong style="color: red">WARNING:</strong> Unfortunately, due to API limitations recently imposed by Spotify <i style="color: violet">(fuck Spotify, for real)</i>, the deployed version of this project isn't able to service more than 25 users at a time. This means your only real option for usage is to locally deploy the application, instructions for which can be found <i style="color: lightgreen; text-decoration: underline">at the bottom of this README.</i></h6>

Playgrate is a web app built using Svelte, Flask, Spotipy, BeautifulSoup, and a few other tools that simplifies transferring your playlists between popular music services (Spotify, Apple Music, the likes). 

Ever transitioned from using one music service to another?
It's generally an absolute pain to try desperately to reconstruct your playlists on whatever new service your job gave you a discount for this week, only to end up giving up and starting a new one *(maybe it's for the best - you and your anime music had to grow apart)*. 

My personal playlist has reached 80 hours of music already, so I know that, if I had to transition services right now, I'd probably just skip the headache and cut my ears off without a tool like Playgrate. Playgrate will feature an intuitive user experience that makes it as easy and simple as it should be to transfer playlists: just select your origin, destination, and the playlist.

---

### CURRENT PROJECT GOALS:
- [X] Integrate Svelte with Flask
- [X] Make underlying back-end modules (need to interface with Apple Music first)
- [X] Design and implement user interface
- [X] Weave together front and back end
- [X] User testing
- [X] Deploy!

---
## How to Locally Deploy:
Unfortunately, because Spotify sucks and hates young devs like me, the only real option for usage of Playgrate is local deployment. <i style="color: lightblue;">Fear not</i> - I will make the process as painless as possible. Make sure your system has the following <strong style="color:magenta">prerequisites:</strong>

- <a href="https://python.org">Python</a>
- <a href="https://nodejs.org">Node.js</a>

NPM is necessary for building the SvelteKit side of things, Python is the actual server. Then, <i style="color:lightblue">clone this repo.</i>
### Step 1: Get your API keys
You'll need to go to the <a href="https://developer.spotify.com/dashboard">Spotify developer dashboard</a> and generate some keys for the API. Log into your Spotify account and go through the process for creating a new app. <i style="color:lightblue">Name it whatever you want.</i> Then, click on your new app in the dashboard. Make a new file in the project's root directory called `.env`, and copy your app's Client ID and Client Secret in the following format:

``````
CLIENT_ID="your-client-id-here"
CLIENT_SECRET="your-client-secret-here"
FLASK_SECRET_KEY="whatever-long-unique-code-you-want"
``````
Then, add `http://localhost:5000` as a Redirect URI in your app settings, and you're good to go!

### Step 2: Set up your Python venv
From the project's root directory, run the following to set up your Python virtual environment (a self-contained environment for packages). 

```python3 -m venv .venv```
### Step 3: Install Python requirements
Use the included <i style="color:pink">requirements.txt</i> file to easily install the Python packages required.

<h5>Windows:</h5>

```.venv\Scripts\pip.exe install -r requirements.txt ```
<h5>Linux:</h5>

```.venv/bin/pip install -r requirements.txt```

### Step 4: Install Node.js packages
Installing the required NPM packages is easy too:

```cd client```

```npm install```

### Step 5: Build and serve!
Run the following command (from the project root) to generate the static site:
```npm run build --prefix client```

And then serve it by simply running the following:

<h5>Windows:</h5>

```.venv\Scripts\python.exe main.py```

<h5>Linux:</h5>

```.venv/bin/python main.py```
<div align="center"><h2>That's it! Now just go to <a href="http://localhost:5000">http://localhost:5000</a> and you're good to go!</h2></div>
<div align="center">
  <a href="https://shipwrecked.hackclub.com/?t=ghrm" target="_blank">
    <img src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/739361f1d440b17fc9e2f74e49fc185d86cbec14_badge.png" 
         alt="This project is part of Shipwrecked, the world's first hackathon on an island!" 
         style="width: 35%;">
  </a>
</div>
