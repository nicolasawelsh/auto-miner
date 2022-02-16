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
        # Extract URL from message
        try:
            # Hard-coded data structure
            contents_url = message.embeds[0].image.url
            if not contents_url: contents_url = False
        except Exception as e:
            contents_url = False
        finally:
            print(f"{contents_url=}")

        # Extract text from message
        try:
            # Hard-coded data structure
            contents_text = message.embeds[0].to_dict()["fields"][-1]["value"]
            if not contents_text: contents_text = False
        except Exception as e:
            contents_text = False
        finally:
            print(f"{contents_text=}")

        print()

        if contents_url:
            if not teleport_pattern.search(contents_url):
                print("MONSTER FOUND")
                with open(detection_file, 'w') as fp:
                    fp.write("monster")

        elif contents_text:
            if repair_pattern.search(contents_text):
                print("REPAIR FOUND")
                with open(detection_file, 'w') as fp:
                    fp.write("repair")



if __name__ == "__main__":
    client.run(TOKEN)
