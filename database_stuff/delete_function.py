import psycopg2
from database_stuff.db_config import config
from utils import generate_condition_string

def delete_function(server_id, db_name, condition_names, condition_values):
    condition_string = generate_condition_string(condition_names, condition_values)

    sql = f"""DELETE FROM {db_name} WHERE {condition_string}"""
    print(sql)

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