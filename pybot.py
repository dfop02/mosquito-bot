import re
import json
import random
import asyncio
import discord
from bot_utils import *
from bot_helpers import *

LOL_TIMEOUT = dict()
COOLDOWN = dict()

# Enable ALL intents then everything will work fine
intents = discord.Intents.all()
bot = discord.Client(intents=intents)

########## EVENTS ##########
# Event that happens when bot setup and is ready to work
@bot.event
async def on_ready():
    loads()
    print(f'{bot.user} has connected to Discord!')

# Event that happens when someone is typing a message
@bot.event
async def on_typing(channel, user, when):
    # limit bot to listen just 'main' channel of your guild
    def check(channel, user):
        return user != bot.user and channel.id == CHANNEL_LISTEN_ID

    if check(channel, user):
        pass

# Event that happens when a message is deleted
@bot.event
async def on_message_delete(message):
    # A message was deleted by a moderator.
    # Note that this only triggers if the message was deleted by someone other than the author.
    # To get if user deleted his own message, check last created entry on deleted messages if matches current time
    async for entry in message.guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
        diff = entry.created_at.astimezone(TZ) - datetime.now(TZ)
        deleted_by = entry.user if diff.seconds <= 5 else message.author

    response = None

    if not message.author.bot and event_not_in_cooldown('on_message_delete', 60):
        if deleted_by.id != message.author.id:
            response = 'Alá a puta do {} apagando a {}'.format(
                deleted_by.name,
                'minha msg!' if message.author.name == bot.user.id else f'msg do {message.author.name}!'
            )
        elif deleted_by.id == message.author.id:
            response = 'Alá a puta do {} apagando própria mensagem, ta querendo esconder oq?'.format(
                deleted_by.name
            )

    if response:
        async with message.channel.typing():
            await message.channel.send(response)
            await asyncio.sleep(1)
            await message.channel.send(EMOJIS['pepeCop'])

# When a guild member is banned
@bot.event
async def on_member_ban(guild, user):
    if bot.user.id != user.id:
        await report('Haha one more banned')

# Event that happens on every message
@bot.event
async def on_message(message):
    # limit bot to listen just 'main' channel of your guild
    # and ignore own messages
    def check(message):
        return message.author != bot.user and message.channel.id == CHANNEL_LISTEN_ID

    if check(message):
        # Put here your new method
        await img_block(message)
        await pog(message)
        await normal_response(message)
        await say_in_voice(message)
        await play_in_voice(message)

# Event that happens when someone join, move or left a voice channel
@bot.event
async def on_voice_state_update(member, before, after):
    await alone_in_voice(member, before, after)

# Event that happens when user activities is updated
@bot.event
async def on_presence_update(before, after):
    if before.bot or before.name in ['@everyone', '@here']:
        return

    if any(filter(lambda activity: is_playing(activity.type), before.activities)):
        await playing_lol(before, after)

# Event that happens when some member is banned (including bot itself)
@bot.event
async def on_member_ban(guild, member):
    if member.id == bot.user.id:
        await report(f'HEEEEELP! SOMEONE IS BANNING ME!')
        # You can use some emoji from your guild by add on defaults json
        # await report(EMOJIS['pepeShotgun'])
    else:
        await report(f'HAHA! NEW BAN!')
        # Here other example of emoji
        # await report(EMOJIS['pepeCop'])

# Event that happens right before bot shutdown
@bot.event
async def close():
    global LOL_TIMEOUT, COOLDOWN
    with open('json/saves.json', 'w') as outfile:
        try:
            # Reset LOL_TIMEOUT to only track while BOT on
            save_dict = { 'LOL_TIMEOUT': {}, 'COOLDOWN': COOLDOWN }
            outfile.write(json.dumps(save_dict, default=str))
        except:
            print('Fail to save new entries on json')
########## END EVENTS ##########

# ON READY EVENT
def loads():
    global LOL_TIMEOUT, COOLDOWN
    with open('json/saves.json') as json_file:
        json_loaded = datetime_parser(json.load(json_file))
        LOL_TIMEOUT = json_loaded['LOL_TIMEOUT']
        COOLDOWN = json_loaded['COOLDOWN']

# ON TYPING EVENT
# Check if a specific user is typing
async def user_typing(user):
    if user.id == USERS['USERNAME'] and event_not_in_cooldown(USERS['USERNAME']):
        await asyncio.sleep(2)
        await report(f"Look, <@{USERS['USERNAME']}> digitando ala {EMOJIS['pog']}")

# ON MESSAGE EVENT
# Block user gif or images
async def img_block(message):
    author = message.author
    # Check if message author id is equal to username added on json defaults
    # Check if there is any attachments or gif link
    # Check if event not in cooldown
    if author.id == USERS['USERNAME'] and (message.attachments or find_gif_url(message.content)) and event_not_in_cooldown(USERS['USERNAME']):
            await message.delete()
            await report("Bro, you're not allowed to send img or gif")

# check if someone is using mudae bot
async def no_gift(message):
    author = message.author
    if author.id == USERS['USERNAME'] and all(word in message.content for word in ['$give', f"<@{USERS['RANDOM_ID']}>"]):
        await message.channel.send('You can not give it to him!', reference=message)

# resend some common emoji on your server
async def pog(message):
    # On this case we use just one hour delay
    if message.content == EMOJIS['pog'] and event_not_in_cooldown(EMOJIS['pog'], ONE_HOUR_DELAY):
        await message.channel.send(EMOJIS['pog'])

# normal response some user, but showing bot is typing before send
async def normal_response(message):
    if message.author.id == USERS['USERNAME'] and event_not_in_cooldown(USERS['USERNAME']):
        async with message.channel.typing():
            await message.channel.send('Hello, finally here to fun everyone', reference=message)
            await asyncio.sleep(1)
            await message.channel.send(EMOJIS['pog'])

# send a image
async def send_image(message):
    if event_not_in_cooldown('image_event'):
        # For images you can use discord.File() to send a image/gif from images folder
        await message.channel.send('any optional text goes here', file=discord.File('images/example.png'))
        # Alternatively, you can use URLs for images/gifs by adding the link as a standard message to be sent by your bot.
        # await message.channel.send('https://i.imgur.com/YiMUiop.gif')

# offense someone based on defaults OFFENSES without repeat while bot is on
async def offense_someone(message):
    NO_REPEAT_OFENSAS = []

    if message.content.startswith(f'<@{bot.user.id}>') and 'offense' in message.content.casefold():
        users = re.findall("<@(\d+)>", message.content)
        del users[0]

        if len(users) == 1:
            if NO_REPEAT_OFENSAS == []:
                NO_REPEAT_OFENSAS = OFFENSES
                random.shuffle(NO_REPEAT_OFENSAS)

            user_id = users[0]
            async with message.channel.typing():
                await asyncio.sleep(1)
                await message.channel.send(f'<@{user_id}> {NO_REPEAT_OFENSAS.pop()}')
        elif len(users) > 1:
            await message.channel.send('just one at once')
        else:
            await message.channel.send('if you want me to offense someone, tag he/she here')

# go to a voice channel and say something from text input
async def say_in_voice(message):
    call_bot = message.content.startswith(f'<@{bot.user.id}>')
    call_words = all(word in message.content for word in ['say', 'in', 'voice'])
    text_to_speech = message.content.casefold().split(':')

    # Check if message starts tag the bot
    # Check if message contains "call voice and idiots" like "@bot go to voice channel and say the're idiots""
    # Check if event is in delay
    if call_bot and call_words and event_not_in_cooldown('say_in_voice', ONE_HOUR_DELAY):
        # Get all voice channels on guild
        voice_channels = message.guild.voice_channels
        # Get first voice channel with some user
        voice = next((voice_channel for voice_channel in voice_channels if len(voice_channel.members) >= 1), None)

        if not voice:
            return

        # connect to voice channel
        voice_client = await voice.connect(reconnect=False)
        # Convert text to speech and say it on voice
        try:
            voice_client.play(
                discord.PCMVolumeTransformer(
                    discord.FFmpegPCMAudio(
                        generate_speech_to(text_to_speech[1]),
                        pipe=True
                    ),
                    volume=1.0
                )
            )
        except Exception as e:
            print(e)

        # Avoids leave voice before complete message
        while voice_client.is_playing():
            await asyncio.sleep(1)

        # Disconnect manually from voice
        await voice_client.disconnect()

        # finally say something on main channel about it
        async with message.channel.typing():
            await message.channel.send(f'I went to {voice.name} and said hi')
            await asyncio.sleep(1)
            await message.channel.send(EMOJIS['pog'])

# go to a voice channel and say something from audio file
async def play_in_voice(message):
    call_bot = message.content.startswith(f'<@{bot.user.id}>')
    call_words = all(word in message.content for word in ['voice', 'idiots'])

    # Check if message starts tag the bot
    # Check if message contains "call voice and idiots" like "@bot go to voice channel and say the're idiots""
    # Check if event is in delay
    if call_bot and call_words and event_not_in_cooldown('play_in_voice', ONE_HOUR_DELAY):
        # Get all voice channels on guild
        voice_channels = message.guild.voice_channels
        # Get first voice channel with some user
        voice = next((voice_channel for voice_channel in voice_channels if len(voice_channel.members) >= 1), None)

        if not voice:
            return

        # connect to voice channel
        voice_client = await voice.connect(reconnect=False)
        # Use any .mp3 audio file on audios folder to play here
        voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('audios/hi.mp3')))

        # while playing keep waiting
        while voice_client.is_playing():
            await asyncio.sleep(0.1)

        # disconnect from voice channel
        await voice_client.disconnect()

        # finally say something on main channel about it
        async with message.channel.typing():
            await message.channel.send(f'I went to {voice.name} and said hi')
            await asyncio.sleep(1)
            await message.channel.send(EMOJIS['pog'])

# ON VOICE STATE UPDATE EVENT
# Check if user is alone on voice for more than one hour
async def alone_in_voice(member, before, after):
    if not before.channel and after.channel and member.id == USERS['USERNAME']:
        print(f'{member} has joined the vc')
        await asyncio.sleep(ONE_HOUR_DELAY)

        vc = bot.get_channel(after.channel.id)
        only_zako = len(vc.members) == 1 and any(map(lambda m: m.id == USERS['USERNAME'], vc.members))
        if only_zako and event_not_in_cooldown(USERS['USERNAME']):
            await report('bro, our friend is alone again on voice =/')

# ON PRESENCE UPDATES EVENT
# Check if someone is playing a specific game and do something
async def playing_lol(before, after):
    lol = 'league of legends'

    get_before_activity = lambda activity: is_activity(activity) and is_playing(activity.type) and activity.name.casefold() == lol and activity.timestamps != None
    old = list(filter(get_before_activity, before.activities))
    user_id = str(before.id)

    if any(old):
        get_after_activity = lambda activity: is_activity(activity) and is_playing(activity.type) and activity.name.casefold() == lol
        new = list(filter(get_after_activity, after.activities))

        global LOL_TIMEOUT

        # Keep playing
        if new:
            if not user_id in LOL_TIMEOUT and old[0].start:
                LOL_TIMEOUT[user_id] = { 'start': old[0].start.astimezone(TZ), 'watching': True }
                return

            if not old[0].start:
                return

            current = datetime.now(TZ)
            started = LOL_TIMEOUT[user_id]['start']
            hours = (current - started).seconds//3600

            # When someone keep playing for more than one hour
            if hours >= 1 and LOL_TIMEOUT[user_id]['watching']:
                channel = bot.get_channel(CHANNEL_LISTEN_ID)
                LOL_TIMEOUT[user_id]['watching'] = False

                async with channel.typing():
                    await channel.send(f'Bruh, <@{user_id}> is playing lol for {hours}h, pls stop')
                    await asyncio.sleep(1)
                    await channel.send(EMOJIS['pog'])
    else:
        # Finish playing
        if user_id in LOL_TIMEOUT:
            current = datetime.now(TZ)
            user_stats = LOL_TIMEOUT.pop(user_id)
            started = user_stats['start']
            hours = (current - started).seconds//3600

            # When someone played for more than 1 hour
            if hours >= 1:
                channel = bot.get_channel(CHANNEL_LISTEN_ID)

                async with channel.typing():
                    await channel.send(f'Finally <@{user_id}> stopped, playing for {hours}h')
                    await asyncio.sleep(1)
                    await channel.send(EMOJIS['pog'])

# DEFAULT METHODS
# alias to send message on main channel
async def report(message):
    channel = bot.get_channel(CHANNEL_LISTEN_ID)
    await channel.send(message)

# check if event is in cooldown
def event_not_in_cooldown(user_id, delay_in_seconds=None):
    # You can define delay_in_seconds, default is one day delay
    now = datetime.now(TZ)
    if str(user_id) in COOLDOWN:
        diff = now - COOLDOWN[str(user_id)]

        if (delay_in_seconds and diff.seconds >= delay_in_seconds) or (diff.days >= 1):
            COOLDOWN[str(user_id)] = now
            return True
        else:
            return False
    else:
        COOLDOWN[str(user_id)] = now
        return True

# Boot BOT
bot.run(DISCORD_TOKEN)
