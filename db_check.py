import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_password = os.environ.get("DB_PASSWORD")

def check_database():
    """Check if we can connect to the database and if the article table exists."""
    conn = None
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password=db_password,
            database="gears_of_war"
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM article;")
        count = cursor.fetchone()[0]
        print(f"Found {count} articles in database")
        
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise e
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_database()