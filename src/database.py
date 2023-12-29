import os
import logging
import psycopg2 as psycopg
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

"""
A database class that implements database methods in different layers.
Layer 1: Basic Database interaction.
Layer 2: Data validation checks
Layer 3: Discord interaction.
Layer 4: Syncs and Database jobs
"""


class DB:
    """
    1st Layer.
    From here we create:
    - Basic Database interaction
    """
    logger.info('- Connecting to DB')

    def __init__(self, discord_client):
        """
        Initialize the database, create a connection using the provided
        database connection string, create a cursor and define the client.

        Parameters
        ----------
        discord_client : discord client object
            your discord client object defined in main

        Returns
        -------
        db object
        """
        self.db_host = os.getenv("POSTGRES_HOST")
        self.db_port = os.getenv("POSTGRES_PORT")
        self.db_user = os.getenv("POSTGRES_USER")
        self.db_password = os.getenv("POSTGRES_PASSWORD")
        self.db_name = os.getenv("POSTGRES_DB")
        self.conn_string = (f"postgresql://"
                            f"{self.db_user}:{self.db_password}"
                            f"@{self.db_host}:{self.db_port}"
                            f"/{self.db_name}")
        self.connection = psycopg.connect(self.conn_string)
        self.cursor = self.connection.cursor()
        self.discord_client = discord_client
        logger.debug(f"Connecting to: {self.conn_string}")
        logger.debug(f"Using {discord_client} as discord client")

    def create_cursor(self):
        """
        Create a cursor and return it.

        Returns
        -------
        database cursor
        """
        return self.connection.cursor()

    def close_cursor(self):
        """
        Close the cursor and connection.
        """
        self.cursor.close()
        self.connection.close()

    def commit_query(self):
        """
        Commit the current query
        """
        self.connection.commit()
        self.connection.close()

    def select_one(self, query, *data):
        """
        Execute a query and return the first result.

        Parameters
        ----------
        :param query: A pyscopg query string
        :param data: Data to be passed to the query

        Returns
        -------
        :return: The first result of the query
        """
        self.create_cursor()
        if data:
            self.cursor.execute(query, data)
        else:
            self.cursor.execute(query)
        data = self.cursor.fetchone()
        self.connection.commit()
        return data

    def select_all(self, query, *data):
        """
        Execute a query and return all results.

        Parameters
        ----------
        :param query: A pyscopg query string
        :param data: Data to be passed to the query

        Returns
        -------
        :return: All results of the query
        """
        if data:
            self.cursor.execute(query, data)
        else:
            self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.connection.commit()
        return data

    def update(self, query, data):
        """
        Execute an update query.

        Parameters
        ----------
        :param query: A pyscopg query string
        :param data: The data to be passed to the query

        Returns
        -------
        :return: None - updates the database
        """
        self.cursor.execute(query, (data,))
        self.connection.commit()

    def insert(self, query, data):
        """
        Execute an insert query.

        Parameters
        ----------
        :param query: A pyscopg query string
        :param data: The data to be passed to the query

        Returns
        -------
        :return: None - inserts into the database
        """
        self.cursor.execute(query, (data,))
        self.connection.commit()

    """ 
    2nd Layer.
    From here we create:
    - Existence Checks
    """

    def is_data_in_db(self, table_name, column_name, value):
        """
        Check if a value is in the database.

        Parameters
        ----------
        :param table_name: The name of the table to check
        :param column_name: The name of the column to check
        :param value: the value to pass to the pyscopg query

        Returns
        -------
        :return: boolean - if the data is in the database
        """
        cursor = self.connection.cursor()
        query = f"SELECT * FROM {table_name} WHERE {column_name} = (%s)"
        cursor.execute(query, (value,))
        data = cursor.fetchone()

        if data is None:
            return False
        return True

    def is_guild_in_db(self, guild_id):
        """
        Check if a guild is in the database.

        Parameters
        ----------
        :param guild_id: The id of the guild to check

        Returns
        -------
        :return: boolean - if the guild is in the database
        """
        return self.is_data_in_db("guilds", "discord_guild_id", str(guild_id))

    def is_settings_in_db(self, guild_id):
        """
        Check if the settings for a guild is in the database.

        Parameters
        ----------
        :param guild_id: The id of the guild to check

        Returns
        -------
        :return: boolean - if the settings for a guild are in the database
        """
        return self.is_data_in_db("settings", "discord_guild_id", str(guild_id))

    def is_channel_in_db(self, channel_id):
        """
        Check if a channel is in the database.

        Parameters
        ----------
        :param channel_id: The id of the channel to check

        Returns
        -------
        :return: boolean - if the channel is in the database
        """
        return self.is_data_in_db("channels", "channel_id", str(channel_id))

    def is_member_in_db(self, member_id):
        """
        Check if a member is in the database.

        Parameters
        ----------
        :param member_id: The id of the member to check

        Returns
        -------
        :return: boolean - if the member is in the database
        """
        return self.is_data_in_db("members", "member_id", str(member_id))

    def is_role_in_db(self, role_id):
        """
        Check if a role is in the database.

        Parameters
        ----------
        :param role_id: The id of the role to check

        Returns
        -------
        :return: boolean - if the role is in the database
        """
        return self.is_data_in_db("roles", "role_id", str(role_id))

    def is_command_in_db(self, command_id):
        """
        Check if a command is in the database.

        Parameters
        ----------
        :param command_id: The id of the command to check

        Returns
        -------
        :return: boolean - if the command is in the database
        """
        return self.is_data_in_db("commands", "command_id", str(command_id))

    def get_all_tables_in_database(self):
        """
        Returns a list of all tables in the database

        :return: list - containing all table names in the database
        """
        query = ("SELECT table_name FROM information_schema.tables"
                 " WHERE table_schema='public';")
        return self.select_all(query)
