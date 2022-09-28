import psycopg2
from database_stuff.db_config import config
from utils import list_to_string


def select_function(server_id, db_name, select_list, condition_names, condition_values):

    condition_string = ""

    for index, element in enumerate(condition_names):
        condition_string+=f"{element} = {condition_values[index]}"
        if (index != len(condition_names)-1):
            condition_string+=" AND"


    sql = f"""SELECT {list_to_string(select_list, ",")} from {db_name}
            where {condition_string};"""

    

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
