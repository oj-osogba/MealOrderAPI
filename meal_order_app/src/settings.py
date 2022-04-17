import sqlalchemy
import psycopg2
from decouple import config

conn = psycopg2.connect("""
    dbname=meal_order_app_db user=postgres host=pg port=5432
    """)
SQL_URI = f"postgresql://postgres:{config('DB_PASSWORD')}@pg:5432/meal_order_app_db"
engine = sqlalchemy.create_engine(SQL_URI)
