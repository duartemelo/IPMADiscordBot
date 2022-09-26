import requests
import json
import exceptions


# Returns the name of a city with a specific city_code (passed by argument)
def get_city(city_code):
    try:
        city_code = int(city_code)
    except Exception as e:
        raise e
    city = None
    response = requests.get("https://api.ipma.pt/open-data/distrits-islands.json")
    json_data = json.loads(response.text)

    for city_data in json_data['data']:
        if city_data['globalIdLocal'] == city_code:
            city = city_data['local']

    if city is None:
        raise exceptions.CityDoesNotExist

    return city


# Returns all cities available in the API
def get_all_cities():
    cities = []

    try:
        response = requests.get("https://api.ipma.pt/open-data/distrits-islands.json")
        json_data = json.loads(response.text)

        for city_data in json_data['data']:
            cities.append(city_data['local'])
    except Exception as e:
        print(e)

    return cities


# Returns the city_code of a city with a specific city name (passed by argument)
def get_city_code(city):
    city = city.lower()
    city_code = None

    try:
        response = requests.get("https://api.ipma.pt/open-data/distrits-islands.json")
        json_data = json.loads(response.text)

        for city_data in json_data['data']:
            if city_data['local'].lower() == city:
                city_code = city_data['globalIdLocal']
                break

        if city_code is None:
            raise exceptions.CityDoesNotExist(f"Cidade {city} não existe. $cities para ver lista de cidades")

    except Exception as e:
        raise e
    else:
        return city_code


# Returns the weather for a city
# receives the city code
# receives the day that user wants to get weather info from
def get_weather(city_code, day):  # example: Braga = 1030300 # Day = 0 if today, 1 tomorrow, etc.

    weather = {
        "precipitaProb": None,
        "tMin": None,
        "tMax": None,
        "predWindDir": None,
        "idWeatherType": None,
        "classWindSpeed": None,
        "forecastDate": None,
    }

    response = requests.get(f"http://api.ipma.pt/open-data/forecast/meteorology/cities/daily/{city_code}.json")
    json_data = json.loads(response.text)

    try:
        for key in weather:
            weather[key] = json_data['data'][day][key]
        weather['idWeatherType'] = get_weather_type(weather['idWeatherType'])
    except IndexError:
        raise IndexError("Dia inserido ({day}) inválido. Insira um dia entre 0 (hoje) e 4.")
    except Exception as e:
        raise e

    return weather


# Returns the weather type for a specific idWeatherType
def get_weather_type(weather_id):

    weather_type = None

    try:
        response = requests.get("https://api.ipma.pt/open-data/weather-type-classe.json")
        json_data = json.loads(response.text)

        for weather_type_data in json_data['data']:
            if weather_type_data['idWeatherType'] == weather_id:
                weather_type = weather_type_data['descWeatherTypePT']
                break

        if weather_type is None:
            raise Exception

    except Exception as e:
        print(e)

    return weather_type
