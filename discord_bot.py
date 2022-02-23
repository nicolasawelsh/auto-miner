# Imported libraries
import discord
from dotenv import load_dotenv
from os     import getenv
from re     import compile

# Local libraries
from mine_config import alerts


# Regex patterns to detect events
repair_pattern = compile(r'repair')
teleport_pattern = compile(r'\.gif$')
defeated_pattern = compile(r'defeated the enemy')

detection_file = "detection.txt"

# Load evironment variables from .env
load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
GUILD = getenv('DISCORD_GUILD')

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
    # Read only messages from user: "Mining Simulator"
    if message.author.display_name == "Mining Simulator":
        # If message contains embedded content
        if hasattr(message, "embeds") and message.embeds:
            # Extract URL from message embeds
            try:
                # Hard-coded data structure
                contents_url = message.embeds[0].image.url
                if not contents_url: contents_url = False
            except Exception as e:
                contents_url = False
            finally:
                print(f"{contents_url=}")

            # Extract text from message embeds
            try:
                # Hard-coded data structure
                contents_text = message.embeds[0].to_dict()["fields"][-1]["value"]
                if not contents_text: contents_text = False
            except Exception as e:
                contents_text = False
            finally:
                print(f"{contents_text=}")

            if contents_url:
                if not teleport_pattern.search(contents_url):
                    print("MONSTER FOUND")
                    with open(detection_file, 'w') as fp:
                        fp.write(alerts['monster'])

            elif contents_text:
                if repair_pattern.search(contents_text):
                    print("REPAIR FOUND")
                    with open(detection_file, 'w') as fp:
                        fp.write(alerts['repair'])

            print()
        
        # If message contains regular text
        elif hasattr(message, "content") and message.content:
            if defeated_pattern.search(message.content):
                print(f"{message.content=}")
                print("DEFEAT FOUND")
                print()
                with open(detection_file, 'w') as fp:
                    fp.write(alerts['defeat'])


if __name__ == "__main__":
    client.run(TOKEN)
