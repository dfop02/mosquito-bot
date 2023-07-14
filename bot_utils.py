import json
from os import getenv, path
from dotenv import load_dotenv, find_dotenv
from zoneinfo import ZoneInfo

# SETUP
load_dotenv(find_dotenv('.env.local'))
DISCORD_TOKEN = getenv('DISCORD_TOKEN')
CHANNEL_LISTEN_ID = int(getenv('CHANNEL_LISTEN'))

# TIMEZONE
TZ = ZoneInfo('America/Sao_Paulo')
# YOU CAN CHECK THE LIST OF TIMEZONES USING
# import zoneinfo
# zoneinfo.available_timezones()

# DELAY OPTIONS (IN SECONDS)
ONE_DAY_DELAY = 86400
ONE_HOUR_DELAY = 3600

# DEFAULTS
# MOST COMMON EMOJIS FROM SERVER
EMOJIS = {}

# USERS IDS FROM GUILD FOR USE ON SPECIAL EVENTS
USERS = {}

# LIST OF OFFENSES
OFFENSES = []

# LOAD DEFAULTS
def load_defaults():
    global EMOJIS, USERS, OFFENSES
    defaults_file = 'json/defaults.local.json'
    has_default_local = path.exists(defaults_file)

    if not has_default_local:
        defaults_file = defaults_file.replace('.local', '')

    with open(defaults_file) as defaults_json:
        defaults = json.load(defaults_json)
        EMOJIS = defaults['EMOJIS']
        USERS = defaults['USERS']
        OFFENSES = defaults['OFFENSES']

# Load when import
if __name__ != '__main__':
    load_defaults()
