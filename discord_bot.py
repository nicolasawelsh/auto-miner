# Imported libraries
import os
import discord
from dotenv import load_dotenv
import re


repair_pattern = re.compile(r'repair')
teleport_pattern = re.compile(r'\.gif$')
detection_file = "detection.txt"


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
    if hasattr(message, "embeds") and message.embeds:
        # Checks if message has embedded url to image
        if message.embeds[0].image.url:
            print(message.embeds[0].image.url)
            if not teleport_pattern.search(message.embeds[0].image.url):
                # MONSTER FOUND
                print("MONSTER FOUND")
                with open(detection_file, 'w') as fp:
                    fp.write("monster")

        else:
            try:
                contents = (message.embeds[0].to_dict()["fields"][-1]["value"])
            except Exception as e:
                print(e)
            finally:
                print(contents)
            if repair_pattern.search(contents):
                # REPAIR FOUND
                print("REPAIR FOUND")
                with open(detection_file, 'w') as fp:
                    fp.write("repair")



if __name__ == "__main__":
    client.run(TOKEN)
