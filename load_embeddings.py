import os
import json
from openai import OpenAI
import psycopg2
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
db_password = os.environ.get("DB_PASSWORD")

def load_data():
    """Load data from JSON file"""
    with open('data.json', 'r') as file:
        return json.load(file)

def generate_embeddings(batch_size=100):
    # Connect to Postgres
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password=db_password,
        database="gears_of_war"
    )
    cursor = conn.cursor()

    try:
        article = load_data()
        
        # Process articles in batches
        for i in range(0, len(article), batch_size):
            batch = article[i:i + batch_size]
            
            # Prepare batch data
            batch_contents = []
            batch_metadata = []
            
            for article in batch:
                # Create content string
                content = f"{article['title']}"
                batch_contents.append(content)
                batch_metadata.append({
                    'title': article['title'],
                    'media': article['media'],
                    'url': article['url'],
                    'content': content
                })
            
            # Create embeddings for the entire batch
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=batch_contents
            )
            
            # Store each embedding with its metadata
            for j, embedding_data in enumerate(response.data):
                metadata = batch_metadata[j]
                embedding = embedding_data.embedding
                
                cursor.execute(
                    """INSERT INTO article 
                       (title, media, url, content, embedding) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (metadata['title'], metadata['media'], metadata['url'], metadata['content'], embedding)
                )
                print(f"Stored embedding for: {metadata['content'][:50]}...")
            
            print(f"Processed batch {i//batch_size + 1}/{(len(article) + batch_size - 1)//batch_size}")

        conn.commit()
        print("All embeddings stored successfully!")

    except Exception as e:
        print("Error generating embeddings:", e)

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    generate_embeddings()