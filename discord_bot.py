# Imported libraries
import os
import discord
from dotenv import load_dotenv
from re     import match


monster = False
repair  = False

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f'{client.user} is connected to ' \
          f'{guild.name} (id: {guild.id})')


@client.event
async def on_message(message):
    global monster
    global repair

    monster = False
    repair  = False

    if hasattr(message, "embeds") and message.embeds:
        # Checks if message has embedded url to image
        if message.embeds[0].image.url:
            # MONSTER FOUND
            monster = True
        else:
            try:
                contents = (message.embeds[0].to_dict()["fields"][-1]["value"])
            except Exception as e:
                print(e)
            finally:
                print(contents)
            if match("repair", contents):
                # REPAIR FOUND
                repair = True


if __name__ == "__main__":
    client.run(TOKEN)