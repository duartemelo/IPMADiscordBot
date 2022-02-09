import psycopg2
from database_stuff.db_config import config


def delete_server_city(server_id, city_code):
    sql = f"""DELETE FROM cities 
    WHERE city_code = {city_code} AND server_id = {server_id}"""

    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (server_id, city_code))
        conn.commit()
        cur.close()
    except Exception as e:
        raise e
    finally:
        if conn is not None:
            conn.close()
