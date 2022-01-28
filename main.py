import discord
import os
from dotenv import load_dotenv

import data_grabbing
import utils


client = discord.Client()


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("Telling you weather infos. $help for help."))
    print('I logged in as {0.user}'.format(client))


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


# Return the message to send to the user, depending on the received message from the user
def get_message_to_send(message):

    commands = ["cities", "weather", "help"]

    command = message.split()[0]
    arguments = message.split()[1:]
    arguments_string = utils.list_to_string(arguments, " ")


    #TODO organize
    if command in commands:
        if command == commands[0]: # cities list
            message_to_send = f"**Cidades disponíveis:**\n{utils.list_to_string(data_grabbing.get_all_cities(), '; ')}"
        elif command == commands[1]: # weather for a city
            city_code = data_grabbing.get_city_code(arguments_string)
            if city_code == None:
                message_to_send = f"{message} não existe na lista de cidades. ${commands[0]} para ver a lista."
            else:
                message_to_send = f"{data_grabbing.get_weather(city_code, 0)}"

        elif command == commands[2]: # help
            n1 = "\n"
            message_to_send = f"**Comandos disponíveis:**\n{utils.list_to_string(commands, f';{n1}')}"

        else: # command is in list, but not implemented
            message_to_send = "Esse comando existe, mas a sua resposta está em desenvolvimento."

    else: # command does not exist
        message_to_send = "Comando não existe."

    return message_to_send


load_dotenv()

client.run(os.getenv('TOKEN'))

