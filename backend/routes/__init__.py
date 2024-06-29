import os

from dotenv import load_dotenv

load_dotenv(".env")

os.environ["POSTGRESQL_CONNECTION_STRING"] = os.getenv("POSTGRESQL_CONNECTION_STRING")
