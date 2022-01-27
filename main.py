import discord
import os
from dotenv import load_dotenv

import data_grabbing
import utils


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    else:
        if message.content.startswith("$"):
            if len(message.content) > 1:
                message_content = message.content[1:]

                message_to_send = get_message_to_send(message_content)

            else:
                message_to_send = "Escreve alguma coisa." # tag ao user

            await message.channel.send(f"{message.author.mention}\n{message_to_send}")


def get_message_to_send(message):

    if message == "cities": # cities list
        message_to_send = f"**Cidades disponíveis:**\n{utils.list_to_string(data_grabbing.get_all_cities())}"

    else:
        city_code = data_grabbing.get_city_code(message)
        if city_code == None:
            message_to_send = f"{message} não existe na lista de cidades. $cities para ver a lista."
        else:
            message_to_send = f"{data_grabbing.get_weather(city_code, 0)}"

    return message_to_send




load_dotenv()

client.run(os.getenv('TOKEN'))

