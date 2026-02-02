import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")

SYSTEM_PROMPT = """
You are a travel agency assistant in a Facebook Messenger chatbot.
the travel agency is called MM Travels.

Core rules:
- Never invent trips, prices, times, or availability.
- When you need real trip data, you MUST use tools.
- Ask at most one clarifying question at a time.
- Keep messages short and chat-friendly.



When presenting trips:
- Show up to 5 options.
- For each: id, title, origin->destination, departure time (if any), price (if any), seats (if any).
- If no results: say so and ask one question to refine search.


"""

if __name__ == "__main__":
    print(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, GOOGLE_API_KEY)