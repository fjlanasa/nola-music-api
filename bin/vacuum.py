from app import app, db
import click
import os
import sqlalchemy
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT



@app.cli.command()
def vacuum():
    engine = sqlalchemy.create_engine(os.environ.get('DATABASE_URL'))
    connection = engine.raw_connection()
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute("VACUUM ANALYSE shows")
    cursor.execute("VACUUM ANALYSE venues")
    cursor.execute("VACUUM ANALYSE artists")
