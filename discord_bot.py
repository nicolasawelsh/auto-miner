# Imported libraries
import discord
from dotenv import load_dotenv
from os     import getenv

# Local libraries
from config.message   import Message_Dissection
from config.pickle_db import read_db, write_db


# Load environment variables from .env
load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
GUILD = getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            print(f'{client.user} is connected to '
                  f'{guild.name} (id: {guild.id})')
            break


@client.event
async def on_message(message):
    message_dissected = Message_Dissection(message)
    print(message_dissected.__dict__)

    if message_dissected.is_bot():
        db = read_db()
        if message_dissected.repair_needed():
            print("REPAIR NEEDED")
            db['repair_needed'] = True
        elif message_dissected.repair_success():
            print("REPAIR SUCCESS")
            db['repair_needed'] = False
        elif message_dissected.monster_appeared():
            print("MONSTER APPEARED")
            db['monster_appeared'] = True
        elif message_dissected.monster_defeated():
            print("MONSTER DEFEATED")
            db['monster_appeared'] = False
        write_db(db)
        print()


if __name__ == "__main__":
    try:
        client.run(TOKEN)
    except Exception as e:
        print('Failed to connect bot to server!')
        print(e)
