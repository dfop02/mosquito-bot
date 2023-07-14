# Mosquito Bot
A discord bot made in python to joke your friends in your discord server

### What is this Bot?
This Bot was made just to joke my friends, but after a while I notice that become a interesting to share it. Basically a collection of default uses from discord.py, so if you need some operations you may find it here.

## Setup
You'll need use Python >= 3.11

Clone this repo using
```bash
git clone git@github.com:dfop02/mosquito-bot.git
```
join `mosquito-bot` folder and install dependences using
```bash
pip install -r requeriments.txt
```
then create a copy of `.env` and save as `.env.local` filling the environments variables.

## How create a Bot to use this project?
In order to create a new Bot for use this project, you can read [here](https://discord.com/developers/docs/getting-started) step-by-step how create it. After that, we'll need the token generated, put it on the new `.env.local` file you created by this way:
```env
DISCORD_TOKEN='YOUR_TOKEN_HERE'
```

In order to get the ID from users, emojis and channels you first need enable the developer option on your discord.

To enable it, first make sure you have a payment method on file in User Settings -> Billing. Then:

* Open up the Discord app
* Click on the settings cog in the bottom left corner
* Go to Appearance -> allll the way at the bottom
* Toggle "Developer Mode" on and "Application Test Mode" on, and enter your application ID
* Exit user settings

Now click with your right click and the last options will always be the ID, so get the ID from the main channel that bot will run and add to `.env.local`

## Build your own defaults
If you open the file `json/defaults.json` you'll find a new variables and examples that represent content from your server, you can add there to use on bot as you want, you can also copy the file as `json/defaults.local.json` with your content.

## Create your own events
Mosquito Bot already uses few different events on main code, but if you needs extend it, you can check all avaiable events on [Discord.py Docs](https://discordpy.readthedocs.io/en/latest/api.html#event-reference), also can check which methods and attributes each Model has and what it does, well documented.

On code, you can just add a new event like:
```python
@bot.event
def on_invite_create(invite):
    # Do something
    pass
```

All events written will be automatically working when bot runs, so you just need worry about the trigger for event happens and what he should does.

## Author

* [Diogo](https://github.com/dfop02)
