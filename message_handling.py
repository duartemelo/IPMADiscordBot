import utils
import data_grabbing
import message_prettify

backslash_n = "\n"  # created because of the impossibility of using \n inside f strings

commands_templates = {
    "cities": "$cities",
    "weather": "$weather <city> <day>",
    "help": "$help"
}

commands = {
    "cities": lambda args: message_prettify.cities_list_prettify(data_grabbing.get_all_cities()),
    "weather": lambda args: get_message_to_send_weather_for_city(args),
    "help": lambda args: message_prettify.help_prettify(commands),
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

    else:  # command does not exist
        message_to_send = message_prettify.error_prettify("Esse comando não existe")

    return message_to_send


# Returns the message to send to the user when he does $weather <city>
# TODO: pass the day as arg and receive the day from the user
def get_message_to_send_weather_for_city(given_city):
    if given_city == "":
        return message_prettify.error_prettify(commands_templates["weather"])

    city_code = data_grabbing.get_city_code(given_city)
    if city_code is None:
        keys_list = list(commands)
        message_to_send = message_prettify.error_prettify(
            f"{given_city} não existe na lista de cidades. ${keys_list[0]} para ver a lista."
        )
    else:
        weather_dict = data_grabbing.get_weather(city_code, 0)
        message_to_send = message_prettify.get_weather_prettify(weather_dict, city_code)

    return message_to_send
