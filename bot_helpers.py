import re
import discord
from io import BytesIO
from gtts import gTTS
from bot_utils import TZ, USERS
from datetime import datetime

# HELPERS
# Convert string datetime from json to datetime object
def datetime_parser(dct):
    for user_id, values in dct['LOL_TIMEOUT'].items():
        try:
            dct['LOL_TIMEOUT'][user_id]['start'] = datetime.fromisoformat(values['start'])
        except:
            pass

    for user_id, value in dct['COOLDOWN'].items():
        try:
            dct['COOLDOWN'][user_id] = datetime.fromisoformat(value)
        except:
            pass

    return dct

# Generate a speech voice buffer
def generate_speech_to(text):
    buffer = BytesIO()
    gTTS(text).write_to_fp(buffer)
    buffer.seek(0)
    return buffer

# Save generated speech voice in audios folder
def generate_speech_to(text):
    gTTS(text).save('audios/audio_name.mp3')

# Validate if is an activity model
def is_activity(activity):
    return activity.__class__.__name__ == 'Activity'

# Validate if activity is type 'playing'
def is_playing(activity_type):
    return activity_type == discord.ActivityType.playing

# Regex to find gif url
def find_gif_url(string):
    # Regex to find the URL that has with .gif references
    regex = r"https?://.*/.*[-|_|.]gif"
    return re.findall(regex, string)
