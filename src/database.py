import os
import logging
import psycopg2 as psycopg
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
# Load environment variables from the .env file
load_dotenv()

# Retrieve PostgreSQL connection parameters from environment variables
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")

# Construct the connection string
conn_string = f"host={db_host} port={db_port} user={db_user} password={db_password} dbname={db_name}"

# Establish a connection to the PostgreSQL database
def connect_to_db():
    try:
        connection = psycopg.connect(conn_string)
        logger.info(f"Connected to {db_name}!")
        logger.info(f" - Host: {db_host}!")
        logger.info(f" - Port: {db_port}!")

    except psycopg.Error as e:
        print(f"Unable to connect to {db_name}. Error: {e}")

    # finally:
    #     # Close the connection when done
    #     if connection:
    #         connection.close()
    #         print("Connection closed.")