import json
import psycopg2

class PostgresConn(object):
    """Postgres DB Connection"""


    def __init__(self):
        credentials = None
        with open('pg_cred') as f:
            credentials = json.load(f)

        self.username = credentials.get('username')
        self.password = credentials.get('password')
        self.hostname = credentials.get('host_name')
        self.port = credentials.get('port')
        self.dbname = credentials.get('db_name')
        self.conn = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(
                database=self.dbname,
                host=self.hostname,
                user=self.username,
                password=self.password
                )
            return self.conn
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.conn.close()
        except psycopg2.DatabaseError:
            pass
