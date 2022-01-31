import discord
import os
from dotenv import load_dotenv
import message_handling


client = discord.Client()

prefix = "$"

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Telling you weather infos. $help for help."))
    print('I logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    else:
        if message.content.startswith(prefix):
            if len(message.content) > 1:
                message_content = message.content[1:]
                message_to_send = message_handling.get_message_to_send(message_content)

            else:
                message_to_send = "Escreve alguma coisa."  # tag ao user

            if type(message_to_send) == discord.embeds.Embed:  # if its embed
                await message.channel.send(embed=message_to_send)
            else: # if its not embed
                await message.channel.send(f"{message.author.mention}\n{message_to_send}")


load_dotenv()

client.run(os.getenv('TOKEN'))

