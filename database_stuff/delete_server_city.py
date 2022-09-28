import psycopg2
from database_stuff.db_config import config
from database_stuff.delete_function import delete_function


def delete_server_city(server_id, city_code):

    return delete_function(server_id, "cities", ["city_code", "server_id"], [city_code, server_id])