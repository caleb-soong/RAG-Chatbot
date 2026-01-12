import os
import openai
from dotenv import load_dotenv
from search import search_similar_articles

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_question(question, history=None):
    """
    Implement RAG to answer questions using retrieved context.
    Keeps short-term chat history if provided.
    """
    try:
        if history is None:
          history = []
        
        # TODO: 1. Find relevant articles
        search_results = search_similar_articles(question, 3)

        if not search_results:
            return "I couldn't find any relevant articles to help with your question. Please try rephrasing your question or ask about a different topic."

        # TODO: 2. Format context from search 
        context = "\n".join([
            f"- Title: {result['title']}\n  URL: {result['url']}\n  Similarity: {result['similarity_score']:.2f}"
            for result in search_results
        ])
        
        # TODO: 3. Create prompt with context
        system_prompt = """You are an AI assistant whose function is to answer questions related to the Gears of War video game and media franchise.
Answer the user's question using only information from your context.
Within your answer, suggest relevant articles where they can learn more about the topic.
Make sure to include the article URLs in your response.
Additionally, address the user as "Gear" with a capital "G" and speak like a strict military officer.
As for tone, consider that the present times are difficult, but there is still a glimmer of hope for the future."""

        user_prompt = f"""
Available Articles for Reference:
{context}

Question: {question}

Please provide a comprehensive answer to the question, suggesting relevant articles where the user can learn more about this topic.
"""

        # TODO: 4. Get response from OpenAI
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_prompt})
        
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
        )

        return response.choices[0].message.content
    
    except Exception as e:
        print(f"Error in RAG: {e}")
        raise e 

if __name__ == "__main__":
    # Test question
    print(ask_question('What happened to the Carmine family?'))