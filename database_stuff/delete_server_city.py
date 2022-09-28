import psycopg2
from database_stuff.db_config import config
from database_stuff.delete_function import delete_function


def delete_server_city(server_id, city_code):

    delete_function(server_id, "cities", ["city_code", "server_id"], [city_code, server_id])

    # sql = f"""DELETE FROM cities 
    # WHERE city_code = {city_code} AND server_id = {server_id}"""

    # conn = None

    # try:
    #     params = config()
    #     conn = psycopg2.connect(**params)
    #     cur = conn.cursor()
    #     cur.execute(sql, (server_id, city_code))
    #     conn.commit()
    #     cur.close()
    # except Exception as e:
    #     raise e
    # finally:
    #     if conn is not None:
    #         conn.close()