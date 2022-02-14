import psycopg2
from database_stuff.db_config import config
import exceptions

def insert_server_schedule(server_id, schedule):
    sql = f"""INSERT INTO schedule(server_id, schedule)
            VALUES ({server_id}, {schedule});"""

    conn = None

    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (server_id, schedule))
        conn.commit()
        cur.close()
    except psycopg2.errors.UniqueViolation:
        raise exceptions.DuplicateValue("Este servidor já tem uma hora definida.")
    except Exception as e:
        raise e
    finally:
        if conn is not None:
            conn.close()

