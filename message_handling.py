import utils
import data_grabbing
import message_prettify

backslash_n = "\n" # created because of the impossibility of using \n inside f strings

commands = {
    "cities": lambda args: message_prettify.cities_list_prettify(data_grabbing.get_all_cities()),
    "weather": lambda args: get_message_to_send_weather_for_city(args) if args != "" else "**Insere uma cidade**",
    "help": lambda args: f"**Comandos disponíveis:**\n{utils.list_to_string(commands, f';{backslash_n}')}"
}


# Returns the message to send to the user, depending on the received message from the user
def get_message_to_send(message):

    message_to_list = message.split()

    command = message_to_list[0]
    arguments = message_to_list[1:]
    arguments_string = utils.list_to_string(arguments, " ")

    if command in commands:
        func = commands[command]
        message_to_send = func(arguments_string)

    else: # command does not exist
        message_to_send = "Esse comando não existe."

    return message_to_send


# Returns the message to send to the user when he does $weather <city>
def get_message_to_send_weather_for_city(given_city):

    city_code = data_grabbing.get_city_code(given_city)
    if city_code is None:
        keys_list = list(commands)
        message_to_send = f"{given_city} não existe na lista de cidades. ${keys_list[0]} para ver a lista." #fix, dynamic help command
    else:
        message_to_send = f"{data_grabbing.get_weather(city_code, 0)}"

    return message_to_send
