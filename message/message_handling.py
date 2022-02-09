import utils
from data import data_grabbing
from message import message_prettify
from database_stuff.insert_server_city import insert_server_city

backslash_n = "\n"  # created because of the impossibility of using \n inside f strings

# Commands templates, basically how a command should be used
commands_templates = {
    "cities": "$cities",
    "weather": "$weather <city> <day (from 0 to 4)>",
    "help": "$help",
    "setCity": "$setCity <city>"
}

# Commands and their functionalities
commands_functionalities = {
    "cities": lambda *args: message_prettify.cities_list_prettify(data_grabbing.get_all_cities()),
    "weather": lambda *args: get_message_to_send_weather_for_city(args[0]),
    "help": lambda *args: message_prettify.help_prettify(commands_templates),
    "setCity": lambda *args: set_city_handler(*args)
}


# Returns the message to send to the user, depending on the received message from the user
def get_message_to_send(message, server_id):

    message_to_list = message.split()  # separates the message string to a list

    command = message_to_list[0]  # the command is the first index of the list
    arguments = message_to_list[1:]  # the arguments are all the other indexes, from the second to the last one
    arguments_string = utils.list_to_string(arguments, " ")  # passes the arguments to a string

    if command in commands_functionalities:  # if the command is available / created
        func = commands_functionalities[command]
        try:
            message_to_send = func(arguments_string, server_id)
        except Exception as e:
            message_to_send = message_prettify.error_prettify(e)

    else:  # command does not exist
        keys_list = list(commands_templates.values())
        message_to_send = message_prettify.error_prettify(
            f"O comando {command} não existe. {keys_list[2]} para ver os comandos disponíveis."
        )

    return message_to_send


# Returns the message to send to the user when he does $weather <city>
def get_message_to_send_weather_for_city(args):
    args_separated = args.split(" ")

    if len(args_separated) < 2:
        return message_prettify.error_prettify(commands_templates["weather"])  # user did not write the day

    else:
        given_city = args_separated[0]
        day = int(args_separated[1])

        try:
            city_code = data_grabbing.get_city_code(given_city)
        except Exception as e:
            message_to_send = message_prettify.error_prettify(e)
        else:
            try:
                weather_response = data_grabbing.get_weather(city_code, day)
                message_to_send = message_prettify.get_weather_prettify(weather_response, city_code)
            except Exception as e:
                message_to_send = message_prettify.error_prettify(e)

        return message_to_send


# Handles the set city command, receives the city_name and the server_id as arguments
# calls insert_server_city that does the database stuff
def set_city_handler(*args):
    city_name, server_id = args

    try:
        city_code = data_grabbing.get_city_code(city_name)
    except Exception as e:
        message_to_send = message_prettify.error_prettify(e)
    else:
        try:
            insert_server_city(server_id, city_code)
        except Exception as e:
            message_to_send = message_prettify.error_prettify(e)
        else:
            message_to_send = message_prettify.default_message_prettify("Cidade inserida com sucesso.")

    return message_to_send
