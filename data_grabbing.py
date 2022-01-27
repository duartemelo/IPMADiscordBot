import requests
import json


# Returns the name of a city with a specific city_code (passed by argument)
def get_city(city_code):
    city = None
    response = requests.get("https://api.ipma.pt/open-data/distrits-islands.json")
    json_data = json.loads(response.text)

    for city_data in json_data['data']:
        if city_data['globalIdLocal'] == city_code:
            city = city_data['local']

    return city


def get_all_cities():
    cities = []

    response = requests.get("https://api.ipma.pt/open-data/distrits-islands.json")
    json_data = json.loads(response.text)

    for city_data in json_data['data']:
        cities.append(city_data['local'])

    return cities

# Returns the city_code of a city with a specific city name (passed by argument)
def get_city_code(city):
    city = city.lower()
    city_code = None
    response = requests.get("https://api.ipma.pt/open-data/distrits-islands.json")
    json_data = json.loads(response.text)

    for city_data in json_data['data']:
        if city_data['local'].lower() == city:
            city_code = city_data['globalIdLocal']

    return city_code


def get_weather(city_code, day): # Braga 1030300 # Day = 0 if today, 1 tomorrow, etc.
    response = requests.get(f"http://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{city_code}.json")
    json_data = json.loads(response.text)


    minTemp =  json_data['data'][day]['tMin']
    maxTemp = json_data['data'][day]['tMax']

    weatherFinal = f"**Temperatura em {get_city(city_code)}**\nMinimas: {minTemp}\nMaximas: {maxTemp}"

    return weatherFinal


