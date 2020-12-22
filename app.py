from flask import Flask
from flask_restful import Resource, Api
import psycopg2
import json
from configparser import ConfigParser

# app = Flask(__name__)
# api = Api(app)

# class 

def config(filename='db.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect():
    """
    Connect to Postgresql database docker server
    """
    conn = None
    try:
        params = config()

        print('Connecting to Postgresql database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print('Postgresql database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed')

if __name__ == '__main__':
    connect()
