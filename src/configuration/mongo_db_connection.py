import os
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
import pymongo
import certifi

from src.exception import MyException
from src.logger import logging 
from src.constants import MONGODB_URL_KEY , DATABASE_NAME , COLLECTION_NAME

# load the certificate authority file to avoid timeout errors when connecting to MongoDB
ca = certifi.where()

def load_dotenv_if_present() -> None:
    """Load simple key=value pairs from a local .env file into os.environ."""
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not env_path.exists():
        return

    with env_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and value and key not in os.environ:
                os.environ[key] = value


def normalize_mongodb_uri(uri: str) -> str:
    parsed = urlparse(uri)
    if parsed.scheme not in ("mongodb", "mongodb+srv"):
        return uri

    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.setdefault("retryWrites", "true")
    query.setdefault("w", "majority")
    if "tls" not in query and parsed.scheme == "mongodb+srv":
        query["tls"] = "true"

    return urlunparse(parsed._replace(query=urlencode(query)))

load_dotenv_if_present()

class MongoDBClient:
    """
    MongoDBClient is responsible for establishing a connection to the MongoDB database and providing access to the specified collection.
    It uses the pymongo library to interact with MongoDB and handles any exceptions that may occur during the connection process.

    client - MongoClient object that represents the connection to the MongoDB server.

    Methods:
    __init__ (database_name: str) -> None
    """

    client = None

    def __init__(self , database_name: str = DATABASE_NAME) -> None:
        """
        Initailize the MongoDB Connection with the specified database name. It retrieves the MongoDB URL from environment variables, establishes a connection to the MongoDB server, and sets up the client for database operations. If any error occurs during this process, it raises a custom MyException with detailed error information.
        Raises:
        MyException: 
        """

        try:
            #check if a MONGODB client connection has already been established
            if MongoDBClient.client is None:
                # get the MongoDB URL from environment variables
                mongodb_url = os.getenv(MONGODB_URL_KEY)
                if mongodb_url is None:
                    raise MyException(ValueError(f"Environment variable {MONGODB_URL_KEY} is not set"), sys)

                mongodb_url = normalize_mongodb_uri(mongodb_url)
                MongoDBClient.client = pymongo.MongoClient(
                    mongodb_url,
                    tlsCAFile=ca,
                    serverSelectionTimeoutMS=10000,
                    connectTimeoutMS=10000,
                    socketTimeoutMS=10000,
                )
                MongoDBClient.client.admin.command("ping")

            # Use the shared MongoDB client to access the specified database
            self.database = MongoDBClient.client[database_name]
            self.client = MongoDBClient.client
            self.database_name = database_name
            logging.info(f"Successfully connected to MongoDB database: {database_name}")    

        except Exception as e:  
            logging.error(f"Error while connecting to MongoDB: {str(e)}")
            raise MyException(e, sys) from e
