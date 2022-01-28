import discord
import os
from dotenv import load_dotenv

import data_grabbing
import utils


client = discord.Client()

commands = ["cities", "weather", "help"]

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


# Returns the message to send to the user, depending on the received message from the user
def get_message_to_send(message):

    message_to_list = message.split()

    message_len = len(message_to_list)

    command = message_to_list[0]
    arguments = message_to_list[1:]
    arguments_string = utils.list_to_string(arguments, " ")

    if command in commands:
        message_to_send = get_message_to_send_command_handler(command, arguments_string, message_len)

    else: # command does not exist
        message_to_send = "Comando não existe."

    return message_to_send


# Returns the message to send to the user, handles the command received
def get_message_to_send_command_handler(command, arguments_string, message_len):
    if command == commands[0]:  # cities list
        message_to_send = f"**Cidades disponíveis:**\n{utils.list_to_string(data_grabbing.get_all_cities(), '; ')}"

    elif command == commands[1]:  # weather for a city
        if message_len > 1:
            message_to_send = get_message_to_send_weather_for_city(arguments_string)
        else:
            message_to_send = "Introduz uma cidade."

    elif command == commands[2]:  # help
        n1 = "\n"
        message_to_send = f"**Comandos disponíveis:**\n{utils.list_to_string(commands, f';{n1}')}"

    else:  # command is in list, but not implemented
        message_to_send = "Esse comando existe, mas a sua resposta está em desenvolvimento."

    return message_to_send


# Returns the message to send to the user when he does $weather <city>
def get_message_to_send_weather_for_city(given_city):
    city_code = data_grabbing.get_city_code(given_city)
    if city_code == None:
        message_to_send = f"{given_city} não existe na lista de cidades. ${commands[0]} para ver a lista."
    else:
        message_to_send = f"{data_grabbing.get_weather(city_code, 0)}"

    return message_to_send


load_dotenv()

client.run(os.getenv('TOKEN'))

