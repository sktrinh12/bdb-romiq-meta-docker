import psycopg2
import json

credentials = None
with open('pg_cred') as f:
    credentials = json.load(f)

if credentials:
    conn = None
    try:
        conn = psycopg2.connect(
            dbname = credentials.get('db_name'),
            host = credentials.get('host_name'),
            user = credentials.get('username'),
            password = credentials.get('password')
            )
    except Exception as e:
        print(e)


# if __name__ == "__main__":
#     cur = conn.cursor()
#     print('creating cursor')
#     cur.execute('SELECT * FROM META;')
#     cur.close()
#     conn.close()
