import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")




if __name__ == "__main__":
    print(DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, GOOGLE_API_KEY)