import psycopg2
from database_stuff.db_config import config
import exceptions

def insert_server_schedule(server_id, schedule, city_code):
    sql = f"""INSERT INTO schedule(server_id, schedule, city_code)
            VALUES ({server_id}, '{schedule}', {city_code});"""

    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (server_id, schedule))
        conn.commit()
        cur.close()
    except psycopg2.errors.UniqueViolation:
        raise exceptions.DuplicateValue("Este servidor já tem uma hora definida para esta cidade.")
    except Exception as e:
        raise e
    finally:
        if conn is not None:
            conn.close()

