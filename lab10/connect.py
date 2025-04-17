import psycopg2
from config import load_config

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    config = load_config()
    connect(config)
with psycopg2.connect(**config) as conn:
    conn = psycopg2.connect(
        host="localhost",
        database="suppliers",
        user="postgres",
        password="AkhmetMK07"
    )