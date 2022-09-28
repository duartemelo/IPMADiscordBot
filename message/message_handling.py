import sched
from database_stuff.delete_function import delete_function
from database_stuff.select_function import select_function
import utils
from data import data_grabbing
from message import message_prettify
from database_stuff.insert_server_city import insert_server_city
from database_stuff.insert_server_schedule import insert_server_schedule

backslash_n = "\n"  # created because of the impossibility of using \n inside f strings

# Commands templates, basically how a command should be used
commands_templates = {
    "cities": ["$cities", "Ver as cidades disponíveis no IPMA"],
    "weather": ["$weather <city> <day (0 to 4)>", "Ver meteorologia para cidade"],
    "help": ["$help", "Ajuda/comandos"],
    "commands": ["$commands", "Ver comandos"],
    "viewCities": ["$viewCities", "Ver as cidades que estão definidas para o servidor."],
    "setCity": ["$setCity <city>", "Definir uma cidade para este servidor."],
    "deleteCity": ["$deleteCity <city>", "Apagar uma cidade deste servidor."],
    "viewTime": ["$viewTime", "Ver os temporizadores definidos para as cidades do servidor."],
    "setTime": ["$setTime <city> <time>", "Definir um temporizador para uma cidade deste servidor."],
    "deleteTime": ["$deleteTime <city>", "Apagar o temporizador de uma cidade deste servidor."]
}

# Commands and their functionalities
commands_functionalities = {
    "cities": lambda *args: message_prettify.cities_list_prettify(data_grabbing.get_all_cities(), description="Lista de cidades presentes no IPMA."),
    "weather": lambda *args: get_message_to_send_weather_for_city(args[0]),
    "help": lambda *args: message_prettify.help_prettify(commands_templates),
    "commands": lambda *args: message_prettify.help_prettify(commands_templates),
    "viewCities": lambda *args: view_cities_handler(*args),
    "setCity": lambda *args: set_city_handler(*args),
    "deleteCity": lambda *args: delete_city_handler(*args),
    "viewTime": lambda *args: view_time_handler(*args),
    "setTime": lambda *args: set_time_handler(*args),
    "deleteTime": lambda *args: delete_time_handler(*args)
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
        message_to_send = message_prettify.error_prettify(
            f"O comando {command} não existe. $help para ver os comandos disponíveis."
        )

    return message_to_send


# Returns the message to send to the user when he does $weather <city>
def get_message_to_send_weather_for_city(args):
    args_separated = args.split(" ") # separating args

    if len(args_separated) < 2:
        return message_prettify.error_prettify(commands_templates["weather"])  # user did not write the day

    else:
        given_city = args_separated[0] # $weather <city [0]> <day [1]>
        day = int(args_separated[1]) # $weather <city [0]> <day [1]>

        try:
            city_code = data_grabbing.get_city_code(given_city) # get city code (we only have city name)
        except Exception as e:
            message_to_send = message_prettify.error_prettify(e) # some error getting the city_code (city does not exist, for example)
        else:
            try:
                weather_response = data_grabbing.get_weather(city_code, day) # get weather for day specified and city specified
                message_to_send = message_prettify.get_weather_prettify(weather_response, city_code) # "prepare"/"prettify" message to send
            except Exception as e:
                message_to_send = message_prettify.error_prettify(e) # something wrong happened

        return message_to_send


# Returns the message with the cities the user defined for the server
def view_cities_handler(*args): 
    server_id = args[-1]

    try:
        rows = select_function(server_id, "cities", ["city_code"], ["server_id"], [server_id]) # doing a select on the PostgreSQL database
        if len(rows) > 0: # if there is any city defined
            cities = []

            for row in rows:
                cities.append(data_grabbing.get_city(row[0])) # transforming city_codes into city_names
            message_to_send = message_prettify.cities_list_prettify(cities, 1, "Lista de cidades definida para este servidor.")
        else: # no cities defined
            message_to_send = message_prettify.default_message_prettify("Servidor sem cidades.")
    except Exception as e:
        message_to_send = message_prettify.error_prettify(e)

    return message_to_send


# Handles the set city command, receives the city_name and the server_id as arguments
# calls insert_server_city that does the database stuff
def set_city_handler(*args):
    city_name, server_id = args

    if city_name == "":
        return message_prettify.error_prettify(commands_templates["setCity"])

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


# Handles the delete city command, receives the city_name and server_id as arguments
# calls delete_function that does the database related stuff
def delete_city_handler(*args):
    city_name, server_id = args

    if city_name == "":
        return message_prettify.error_prettify(commands_templates["deleteCity"])

    try:
        city_code = data_grabbing.get_city_code(city_name)
    except Exception as e:
        message_to_send = message_prettify.error_prettify(e)
    else:
        try:
            delete_function(server_id, "cities", ["city_code", "server_id"], [city_code, server_id])
            delete_function(server_id, "schedule", ["server_id", "city_code"], [server_id, city_code]) # when deleting a city, it deletes the schedules for that city too
        except Exception as e:
            message_to_send = message_prettify.error_prettify(e)
        else:
            message_to_send = message_prettify.default_message_prettify("Cidade removida com sucesso.")

    return message_to_send



def view_time_handler(*args):
    server_id = args[-1]

    try:
        rows = select_function(server_id, "schedule", ["schedule", "city_code"], ["server_id"], [server_id])
        if len(rows) > 0:
            time = ""
            for row in rows:
                row_time = str(row[0])
                city_code = str(row[1])
                city_name = data_grabbing.get_city(city_code)

                time+=(f"{city_name}, {row_time}\n")
                
            message_to_send = message_prettify.default_message_prettify(time) 
        else:
            message_to_send = message_prettify.default_message_prettify(f"Servidor sem temporizador definido para nenhuma cidade.")
    except Exception as e:
        print(e)
        print(type(e))
        message_to_send = message_prettify.error_prettify(e)

    return message_to_send


# Handles the set time command, receives the schedule (time without time zone) and the server_id as arguments
# calls insert_server_schedule that does the database stuff
def set_time_handler(*args):
    args_separated = args[0].split(" ") # separates city from time ['city', 'time']
    if (len(args_separated) != 2):
        return message_prettify.error_prettify("Comando introduzido incorretamente. Utiliza $help.")
    
    city_name = args_separated[0]
    schedule = args_separated[1]
    server_id = args[-1]
    

    if schedule == "" or city_name == "":
        return message_prettify.error_prettify(commands_templates["deleteTime"])

    try:
        rows = select_function(server_id, "cities", ["city_code"], ["server_id"], [server_id])

        if len(rows) > 0:
            cities = []

            for row in rows:
                cities.append(row[0])
        else:
            return message_prettify.error_prettify("Servidor sem cidades definidas.")
        
        city_code = data_grabbing.get_city_code(city_name)
        if (city_code in cities):            
            try:
                insert_server_schedule(server_id, schedule, city_code)
            except Exception as e:
                message_to_send = message_prettify.error_prettify(e)
            else:
                message_to_send = message_prettify.default_message_prettify("Temporizador adicionado com sucesso.")
        else:
            message_to_send = message_prettify.error_prettify(
                f"A cidade de {city_name} não está adicionada ao servidor, primeiro adicione com $setCity.")

    except Exception as e:
        message_to_send = message_prettify.error_prettify(e)

    return message_to_send


def delete_time_handler(*args):
    server_id = args[-1]
    city_name = args[0]
    if args[0] == "":
        message_to_send = message_prettify.error_prettify("Insere uma cidade.")
        return message_to_send
    city_code = data_grabbing.get_city_code(city_name)

    try:
        delete_function(server_id, "schedule", ["server_id", "city_code"], [server_id, city_code])
    except Exception as e:
        message_to_send = message_prettify.error_prettify(e)
    else:
        message_to_send = message_prettify.default_message_prettify("Temporizador removido com sucesso.")

    return message_to_send
