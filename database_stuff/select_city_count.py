import psycopg2
from database_stuff.db_config import config


def select_city_count(server_id):
    sql = f"""SELECT count(city_code) from cities
            where server_id = {server_id}
            group by server_id"""

    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, server_id)
        result = cur.fetchone()
        if result is None:
            result = 0
        else:
            result = result[0]
        conn.commit()
        cur.close()
        return result
    except Exception as e:
        raise e
    finally:
        if conn is not None:
            conn.close()
