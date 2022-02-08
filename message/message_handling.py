import utils
from data import data_grabbing
from message import message_prettify
from database_stuff.insert_server_city import insert_server_city

backslash_n = "\n"  # created because of the impossibility of using \n inside f strings

# Commands templates, basically how a command should be used
commands_templates = {
    "cities": "$cities",
    "weather": "$weather <city> <day (from 0 to 4)>",
    "help": "$help"
}

# Commands and their functionalities
commands_functionalities = {
    "cities": lambda *args: message_prettify.cities_list_prettify(data_grabbing.get_all_cities()),
    "weather": lambda *args: get_message_to_send_weather_for_city(args[0]),
    "help": lambda *args: message_prettify.help_prettify(commands_functionalities), #TODO: pass the commands_templates here!
    "setCity": lambda *args: set_city_handler(*args)
}


# Returns the message to send to the user, depending on the received message from the user
def get_message_to_send(message, server_id):

    message_to_list = message.split()

    command = message_to_list[0]
    arguments = message_to_list[1:]
    arguments_string = utils.list_to_string(arguments, " ")

    if command in commands_functionalities:
        func = commands_functionalities[command]
        message_to_send = func(arguments_string, server_id)

    else:  # command does not exist
        message_to_send = message_prettify.error_prettify("Esse comando não existe")

    return message_to_send


# Returns the message to send to the user when he does $weather <city>
def get_message_to_send_weather_for_city(args):
    args_separated = args.split(" ")

    if len(args_separated) < 2:
        return message_prettify.error_prettify(commands_templates["weather"])

    else:
        given_city = args_separated[0]
        day = int(args_separated[1])
        city_code = data_grabbing.get_city_code(given_city)
        if city_code is None:  # TODO: exceptions stuff
            keys_list = list(commands_functionalities)
            message_to_send = message_prettify.error_prettify(
                f"{given_city} não existe na lista de cidades. ${keys_list[0]} para ver a lista."
            )
        else:
            weather_response = data_grabbing.get_weather(city_code, day)
            if type(weather_response) is dict:
                message_to_send = message_prettify.get_weather_prettify(weather_response, city_code)
            else:
                message_to_send = message_prettify.error_prettify(weather_response)

        return message_to_send


# Handles the set city command, receives the city_name and the server_id as arguments
# calls insert_server_city that does the database stuff
def set_city_handler(*args):
    city_name, server_id = args

    city_code = data_grabbing.get_city_code(city_name)

    if city_code is None:  # TODO: exceptions stuff
        keys_list = list(commands_functionalities)
        message_to_send = message_prettify.error_prettify(
            f"{city_name} não existe na lista de cidades. ${keys_list[0]} para ver a lista."
        )
    else:
        insert_server_city_response = insert_server_city(server_id, city_code)
        if insert_server_city_response is True:
            message_to_send = message_prettify.default_message_prettify("Cidade inserida com sucesso.")
        else:  # some error TODO: do this with exceptions!
            message_to_send = message_prettify.error_prettify(insert_server_city_response)

    return message_to_send
