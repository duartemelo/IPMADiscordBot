from sys import excepthook
import discord

from data.data_grabbing import get_city
import utils


# fields translations
# the key is the raw field as it comes from the API
# the value is the more beautiful way to show the field name
ui_fields_translations = {
    "precipitaProb": "Probabilidade de precipitação",
    "tMin": "Temperatura mínima",
    "tMax": "Temperatura máxima",
    "predWindDir": "Direção do vento",
    "idWeatherType": "Estado do tempo",
    "classWindSpeed": "Classe de velocidade do vento",
    "forecastDate": "Data da previsão"
}

fields_suffixes = {
    "tMin": "º",
    "tMax": "º",
    "precipitaProb": "%",
}


# Function that returns an embed discord response with the list of all the cities available at IPMA API
# (prettifies the data to be shown)
def cities_list_prettify(cities_list):

    embed_response = discord.Embed(title="Cidades",
                                   description="Lista de cidades",
                                   color=0x6FD9F8)

    embed_response.add_field(name="Cidades",
                             value=utils.list_to_string(cities_list),
                             inline=True)

    return embed_response


# Function that returns an embed discord response with the weather of a city (prettifies the data to be shown)
def get_weather_prettify(weather_dict, city_code):

    embed_response = discord.Embed(title=get_city(city_code),
                                   description="Previsão do tempo",
                                   color=0x6FD9F8)

    for key in weather_dict:
        field_translated = ui_fields_translations[key]
        embed_response.add_field(name=field_translated,
                                 value=handle_field_suffix(key, weather_dict[key]),
                                 inline=False)

    return embed_response


# Function that returns an embed discord response with the help command (shows all the available commands)
def help_prettify(commands):

    embed_response = discord.Embed(title="Comandos disponíveis",
                                   color=0x6FD9F8)

    commands_list = list(commands.keys())

    #TODO: change values_list name
    values_list = []
    descriptions_list = []
    for command in commands_list:
        try:
            values_list.append(commands[command][0])
        except IndexError:
            values_list.append("Sem exemplo.")
        except Exception as e:
            print(e)
        try:
            descriptions_list.append(commands[command][1])
        except IndexError:
            descriptions_list.append("Sem descrição")
        except Exception as e:
            print(e)
        
        


    # values_list = list(commands.values()[0])

    embed_response.add_field(name="Comandos",
                             value=utils.list_to_string(commands_list, "\n"),
                             inline=True)

    embed_response.add_field(name="Exemplo",
                             value=utils.list_to_string(values_list, "\n"),
                             inline=True)

    embed_response.add_field(name="Descrição",
                            value=utils.list_to_string(descriptions_list, "\n"),
                            inline=True)

    return embed_response


# Function that returns an embed discord response with the error response (sends the error message)
def error_prettify(message):
    embed_response = discord.Embed(title="Erro",
                                   color=0xFF0400)

    embed_response.add_field(name="Mensagem",
                             value=message,
                             inline=False)

    return embed_response


# Function that returns an embed discord response with the default message response (sends the message)
def default_message_prettify(message):
    embed_response = discord.Embed(title="Mensagem",
                                   color=0x6FD9F8)

    embed_response.add_field(name="Mensagem",
                             value=message,
                             inline=False)

    return embed_response


# Function that returns the field with its suffix, example:
#                                                  20.0 to 20.0º
#                                                  0.0 to 0.0% (precipitaProb)
# fields_suffixes dictionary has the keys with their suffixes
def handle_field_suffix(key, field_value):

    field_value_str = str(field_value)
    if key in fields_suffixes:
        field_value_str = field_value + fields_suffixes[key]

    return field_value_str
