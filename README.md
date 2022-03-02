# auto-miner
## Automatic Discord Mining Bot

This is a full-package python app to automatically mine on the Discord Mining Simulator.

---

**Features:**
- Mine delay selection
- Pause/Stop macro
- Auto pickaxe repair
- Auto pause and resume on monster

**Requirements:**
- In the current version, you will need a Discord bot account
- Python 3.8
  - The following python modules:
    - [discord](https://pypi.org/project/discord.py/)
    - [pynput](https://pypi.org/project/pynput/)
    - [python-dotenv](https://pypi.org/project/python-dotenv/)

**Setup:**
- Create a [Discord bot account](https://discordpy.readthedocs.io/en/stable/discord.html) and add it to your mining server
- Copy your bot's token
![bot_token](https://github.com/nicolasawelsh/auto-miner/blob/testing/readme/bot_token.png)
- Create a .env file with your bot's token and discord server name in the same directory as this repo
![env](https://github.com/nicolasawelsh/auto-miner/blob/testing/readme/env.png)
- Start the discord bot: `python3 discord_bot.py`
- Start the macro: `python3 macro.py`
