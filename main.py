import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
from message import message_handling, message_prettify

intents = discord.Intents.default()
intents.message_content = True
prefix = "$"

class myclient(discord.Client):

    # bot as logged in
    async def on_ready(self):
        await client.change_presence(activity=discord.Game("Telling you weather infos. $help for help."))
        print('I logged in as {0.user}'.format(client))

    # when the bot receives a message
    async def on_message(self, message):
        # print(f"Message from {message.author}: {message.content}") # Testing purposes


        if message.author == client.user:  # If the message was sent by the bot.
            return

        else:
            server_id = message.guild.id  # server id
        if message.content.startswith(prefix):  # If the message starts with the bot prefix (defined before)
            if len(message.content) > 1:
                message_content = message.content[1:]
                message_to_send = message_handling.get_message_to_send(message_content, server_id)

            else:  # If its only the prefix
                message_to_send = message_prettify.error_prettify(f"Escreve alguma coisa.")

            if type(message_to_send) == discord.embeds.Embed:  # if it's a Discord embed message
                await message.channel.send(embed=message_to_send)
            else:  # if it's not a Discord embed message (should never happen!)
                await message.channel.send(f"{message.author.mention}\n{message_to_send}")


client = myclient(intents=intents)

load_dotenv()  # loading dotenv with the bot token!

client.run(os.getenv('TOKEN'))  # getting the token from the .env file
# if you are getting an error on this, create a .env file with your token (check readme)