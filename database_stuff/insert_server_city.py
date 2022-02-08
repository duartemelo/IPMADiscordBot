import psycopg2
from database_stuff.db_config import config
import exceptions
from data import data_grabbing


def insert_server_city(server_id, city_code):
    sql = f"""INSERT INTO cities(server_id, city_code)
            VALUES ({server_id}, {city_code});"""

    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (server_id, city_code))
        conn.commit()
        cur.close()
        return True
    except psycopg2.errors.UniqueViolation:
        raise exceptions.DuplicateValue(f"A cidade {data_grabbing.get_city(city_code)} já está na base de dados.")
    except Exception as e:
        raise e
    finally:
        if conn is not None:
            conn.close()



