import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_password = os.environ.get("DB_PASSWORD")

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password=db_password,
    database="gears_of_war"
)

cur = conn.cursor()

try:
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS article (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            media TEXT NOT NULL,
            url TEXT NOT NULL,
            content TEXT NOT NULL,
            embedding vector(1536)
        );
    """)
    conn.commit()
    print("Database setup complete!")
except Exception as e:
    print("Error during setup:", e)
finally:
    cur.close()
    conn.close()