import psycopg2
from database_stuff.db_config import config
from database_stuff.select_function import select_function


def select_time(server_id):

    return select_function(server_id, "schedule", ["schedule", "city_code"], ["server_id"], [server_id])

    sql = f"""SELECT schedule, city_code from schedule
            where server_id = {server_id}"""

    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, server_id)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        return result
    except Exception as e:
        raise e
    finally:
        if conn is not None:
            conn.close()
