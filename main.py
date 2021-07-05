import os
import sys

import discord

from bot.template import Context, handle
from bot.tts_bot import TTSConfig, tts_bot

DEBUG = True

TOKEN = ""


def init():
    import bot.tts_bot  # necessary for function
    print(bot.tts_bot)

    if len(sys.argv) <= 1:
        sys.exit("start bot: python main.py <TOKEN>")

    global TOKEN
    TOKEN = sys.argv[1]


if __name__ == "__main__":
    init()

    # create config and line dir
    if not os.path.exists("cfg"):
        os.mkdir("cfg")
    if not os.path.exists("line"):
        os.mkdir("line")

    while True:
        try:
            client = discord.Client()

            online = {}


            @client.event
            async def on_message(message: discord.Message):
                if DEBUG and message.channel.name != "test":
                    return
                author: discord.Member = message.author
                # filter out self message
                if author == client.user:
                    return
                # filter out bot message
                if author.bot:
                    return
                if isinstance(message.channel, discord.DMChannel):
                    await message.channel.send(
                        f"Hi {author.display_name}#{author.discriminator}, please add me to any server in order to use!",
                    )
                    return

                server_id = str(message.guild.id)
                if server_id not in online:
                    online[server_id] = TTSConfig(server_id, os.path.join("cfg", f"cfg_{server_id}.json"), "line")
                await handle(Context(tts_bot, client, online[server_id], message))


            client.run(TOKEN)
        except Exception as e:
            print(f"ERROR: {e}")
