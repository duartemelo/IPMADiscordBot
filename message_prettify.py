import discord
import utils


def cities_list_prettify(cities_list):
    cities_list_first_half = cities_list[:len(cities_list)//2]
    cities_list_second_half = cities_list[len(cities_list)//2:]

    cities_list_first_half_string = utils.list_to_string(cities_list_first_half, "\n")
    cities_list_second_half_string = utils.list_to_string(cities_list_second_half, "\n")

    embed_response = discord.Embed(title="Cidades", description="Lista de cidades disponíveis", color=0x6FD9F8)
    embed_response.add_field(name="Cidades", value=cities_list_first_half_string, inline=True)
    embed_response.add_field(name="+", value=cities_list_second_half_string, inline=True)

    return embed_response

# TODO: weather response

