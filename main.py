import discord
import os
from dotenv import load_dotenv
from message import message_handling, message_prettify

client = discord.Client()

prefix = "$"

# When bot has logged in.
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Telling you weather infos. $help for help."))
    print('I logged in as {0.user}'.format(client))


# When bot receives some message from the user.
@client.event
async def on_message(message):
    if message.author == client.user:  # If the message was sent by the bot.
        return

    else:
        if message.content.startswith(prefix):  # If the message starts with the bot prefix (defined before)
            if len(message.content) > 1:
                message_content = message.content[1:]
                message_to_send = message_handling.get_message_to_send(message_content)

            else:  # If its only the prefix
                message_to_send = message_prettify.error_prettify(f"Escreve alguma coisa.")

            if type(message_to_send) == discord.embeds.Embed:  # if it's a Discord embed message
                await message.channel.send(embed=message_to_send)
            else:  # if it's not a Discord embed message (should never happen!)
                await message.channel.send(f"{message.author.mention}\n{message_to_send}")


load_dotenv()  # loading dotenv with the bot token!

client.run(os.getenv('TOKEN'))  # getting the token from the .env file
# if you are getting an error on this, create a .env file with your token (check readme)
