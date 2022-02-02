import discord

import data_grabbing
import utils


ui_fields_translations = {
    "precipitaProb": "Probabilidade de precipitação",
    "tMin": "Temperatura mínima",
    "tMax": "Temperatura máxima",
    "predWindDir": "Direção do vento",
    "idWeatherType": "ID Estado do tempo",  # TODO: handle this!
    "classWindSpeed": "Classe de velocidade do vento",
    "forecastDate": "Data da previsão"
}

fields_with_degree = ["tMin", "tMax"]


def cities_list_prettify(cities_list):
    cities_list_first_half = cities_list[:len(cities_list)//2]
    cities_list_second_half = cities_list[len(cities_list)//2:]

    cities_list_first_half_string = utils.list_to_string(cities_list_first_half, "\n")
    cities_list_second_half_string = utils.list_to_string(cities_list_second_half, "\n")

    embed_response = discord.Embed(title="Cidades", description="Lista de cidades disponíveis", color=0x6FD9F8)
    embed_response.add_field(name="Cidades", value=cities_list_first_half_string, inline=True)
    embed_response.add_field(name="+", value=cities_list_second_half_string, inline=True)

    return embed_response


def get_weather_prettify(weather_dict, city_code):

    embed_response = discord.Embed(title=data_grabbing.get_city(city_code),
                                   description="Previsão do tempo",
                                   color=0x6FD9F8)

    for key in weather_dict:
        field_translated = ui_fields_translations[key]
        embed_response.add_field(name=field_translated,
                                 value=(str(weather_dict[key]) + "º" if key in fields_with_degree
                                        else str(weather_dict[key])),
                                 inline=False)

    return embed_response

