import json
import psycopg2
import os

class PostgresConn(object):
    """Postgres DB Connection"""


    def __init__(self):

        self.username = os.getenv('UNAME')
        self.password = os.getenv('PASSWORD')
        self.hostname = os.getenv('HOSTNAME')
        self.port = os.getenv('PORT')
        self.dbname = os.getenv('DBNAME')
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
