import psycopg2
from database_stuff.db_config import config


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
    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if conn is not None:
            conn.close()



