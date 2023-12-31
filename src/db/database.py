import os
import logging
import time
import psycopg2 as psycopg
from psycopg2 import OperationalError, Error
from dotenv import load_dotenv
from datetime import datetime
from discord.ext.commands import Bot

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
        self.conn_string = (f"postgresql://"
                            f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
                            f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}"
                            f"/{os.getenv('POSTGRES_DB')}")

        # self.connection = psycopg.connect(self.conn_string)
        # self.cursor = self.connection.cursor()

        self.discord_client = discord_client

        logger.debug(f"Connecting to: {self.conn_string}")
        logger.debug(f"Using {discord_client} as discord client")

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
        connection = psycopg.connect(self.conn_string)
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        data = cursor.fetchone()
        connection.commit()
        connection.close()
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
        connection = psycopg.connect(self.conn_string)
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        data = cursor.fetchall()
        connection.commit()
        connection.close()
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
        connection = psycopg.connect(self.conn_string)
        cursor = connection.cursor()

        cursor.execute(query, data)
        connection.commit()
        connection.close()

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
        connection = psycopg.connect(self.conn_string)
        cursor = connection.cursor()

        cursor.execute(query, data)
        connection.commit()
        connection.close()

    def delete(self, query, data):
        """
        Execute a delete query.

        Parameters
        ----------
        :param query: A pyscopg query string
        :param data: The data to be passed to the query

        Returns
        -------
        :return: None - deletes an entry in the database
        """
        connection = psycopg.connect(self.conn_string)
        cursor = connection.cursor()

        cursor.execute(query, data)
        connection.commit()
        connection.close()

    def healthcheck(self):
        healthy = False
        if not healthy:
            for i in range(5):
                try:
                    with psycopg.connect(self.conn_string):
                        logger.info("PostgreSQL is online and ready to accept connections.")
                        healthy = True
                        break

                except OperationalError as e:
                    logger.critical(f"Error: {e}")
                    logger.critical("PostgreSQL is not available or not ready to accept connections.")
                    logger.critical(f"Retrying in 10 seconds. Attempt #{i}")
                    time.sleep(10)


                except Error as e:
                    logger.critical(f"Error: {e}")
                    logger.critical(f"Retrying in 10 seconds. Attempt #{i}")

                    time.sleep(10)

        if healthy:
            return True

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
        query = f"SELECT * FROM {table_name} WHERE {column_name} = (%s)"
        data = self.select_one(query, (value,))

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
        return self.is_data_in_db("bot_settings", "discord_guild_id", str(guild_id))

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
        return self.is_data_in_db("members", "discord_member_id", str(member_id))

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

    """
    3rd Layer. 
    From here we create:
    - Discord level CRUD commands. Add/remove/update/delete.

    TODO: Add function to add guild when guild does not exist.
    """

    # ---------- Add commands
    def add_guild_to_guilds_table(self, g_name, g_logo, g_created_at, g_member_count, g_nsfw_level
                                  , g_language, discord_guild_id, is_premium, is_test, dt_now):
        """
        Adds a guild to the database, along with all of its corresponding information

        Parameters
        ----------
        :param g_name: the name of the guild
        :param g_logo: the logo of the guild
        :param g_created_at: the datetime when the guild was created
        :param g_member_count: the integer of members in the guild
        :param g_nsfw_level: the nsfw level of the guild
        :param g_language: the primary language of the guild
        :param dt_now: the current datetime
        :param discord_guild_id: the id of the discord guild
        :param is_test: if the guild is a test guild
        :param is_premium: if the guild is a premium guild

        """
        query = """INSERT 
                        INTO guilds
                            (discord_guild_id, name, logo, member_count, nsfw_level
                            , language, is_premium, is_test, created_at, last_sync)
                        VALUES((%s), (%s), (%s), (%s),(%s), (%s), (%s), (%s), (%s), (%s))"""
        try:
            logger.debug(f"Attempting to add guild: {g_name}")
            self.insert(
                query
                , (str(discord_guild_id)
                   , g_name
                   , g_logo
                   , g_member_count
                   , g_nsfw_level
                   , g_language
                   , is_premium
                   , is_test
                   , g_created_at
                   , dt_now)
            )
        except Exception as e:
            logger.warning(f"Failed to add guild '{g_name}' to database. Error: {e}")

    def add_settings_to_bot_settings_table(self, discord_guild_id, discord_member_id, admin, moderation
                                           , logs, antispam, fun, dt_now):
        """
        Adds guild settings to the database

        Parameters
        ----------
        :param discord_guild_id: the id of the discord guild
        :param discord_member_id: the id of the discord bot
        :param admin: the admin flag
        :param logs: the logging flag
        :param moderation: the moderation flag
        :param antispam: the antispam flag
        :param fun: the fun flag
        :param dt_now: the current datetime
        """

        query = """
        INSERT INTO bot_settings
            (discord_guild_id, discord_bot_id, admin, logging, moderation, antispam, fun, last_sync)
        VALUES((%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s));
                """
        try:
            logger.debug(f"Attempting to add bot_settings to guild ID: {discord_guild_id}")
            self.insert(
                query
                , (str(discord_guild_id)
                   , discord_member_id
                   , admin
                   , logs
                   , moderation
                   , antispam
                   , fun
                   , dt_now
                   )
            )
        except Exception as e:
            logger.warning(f"Failed to add bot_settings for guild ID: '{discord_guild_id}' to database. Error: {e}")

    def add_channel_to_channel_table(self, guild_id, channel_id, name, category
                                     , position, mention, jump_url, permissions_synced
                                     , overwrites, created_at, last_synced):
        """
        Adds all guild channel information to the database

        Parameters
        ----------
        :param guild_id: the id of the guild
        :param channel_id: the id of the channel
        :param name: the name of the channel
        :param category: the category of the channel
        :param position: the position of the channel
        :param mention: the mention of the channel
        :param jump_url: the jump url of the channel
        :param permissions_synced: the permissions synced of the channel
        :param overwrites: the overwrites of the channel
        :param created_at: the datetime when the channel was created
        :param last_synced: the datetime when the channel was last synced

        """
        query = """INSERT 
                        INTO channels (
                            discord_guild_id
                            , channel_id
                            , channel_name
                            , category
                            , position
                            , mention
                            , jump_url
                            , permissions_synced
                            , overwrites
                            , created_at
                            , last_synced
                            )
                        VALUES((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))
                            """
        try:
            logger.debug(f"Adding channel:{name} to: {guild_id}")
            self.insert(
                query, (
                    str(guild_id)
                    , str(channel_id)
                    , name
                    , category
                    , position
                    , mention
                    , jump_url
                    , permissions_synced
                    , overwrites
                    , created_at
                    , last_synced
                )
            )
        except Exception as e:
            logger.warning(f"Failed to add channel '{name}' in Guild ID: '{guild_id}' to database. Error: {e}")

    def add_member_to_members_table(self, guild_id, member_id, name, avatar, nickname
                                    , display_name, top_role, created_at, joined_at, last_synced):
        """
        Adds member from a specified guild to the database

        Parameters
        ----------
        :param guild_id: the id of the guild
        :param member_id: the id of the member
        :param name: the name of the member
        :param avatar: the avatar of the member
        :param created_at: the datetime when the member was created
        :param nickname: the nickname of the member
        :param display_name: the display name of the member
        :param top_role: the top role of the member
        :param joined_at: the datetime when the member joined the guild
        :param last_synced: the datetime when the channel was last synced

        """
        query = """INSERT 
                        INTO members
                            (discord_guild_id, discord_member_id, name, avatar, nickname
                            , display_name, top_role, joined_at, created_at, last_sync)
                        VALUES((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))
                            """
        try:
            logger.debug(f"Adding member:{name} to: {guild_id}")
            self.insert(query,
                        (str(guild_id), str(member_id), name, avatar, nickname
                         , display_name, top_role, joined_at, created_at, last_synced))
        except Exception as e:
            logger.warning(f"Failed to add member '{name}, {member_id}' in Guild ID: '{guild_id}' to database."
                           f" Error: {e}")

    def add_role_to_roles_table(self, id_guild, role_id, role_name, position, color
                                , hoisted, mentionable, managed, permissions, created_at
                                , last_synced):
        """
        Adds all roles from a specified guild to the database

        Parameters
        ----------
        :param id_guild: the id of the guild
        :param role_id: the id of the role
        :param role_name: the name of the role
        :param position: the position of the role
        :param color: the color of the role
        :param hoisted: If the role is seperated in the members tab
        :param mentionable: If the role is mentionable or not
        :param managed: If the role is managed or not
        :param permissions: the permissions of the role
        :param created_at: the datetime when the role was created
        :param last_synced: the datetime when the role was last synced

        """
        query = """INSERT 
                        INTO roles (
                            discord_guild_id
                            , role_id
                            , role_name
                            , position
                            , color
                            , hoisted
                            , mentionable
                            , managed
                            , permissions
                            , created_at
                            , last_synced
                            )
                        VALUES((%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s),(%s))
                            """
        try:
            logger.debug(f"Adding role:{role_name} to: {id_guild}")
            self.insert(
                query, (
                    str(id_guild)
                    , str(role_id)
                    , role_name
                    , position
                    , color
                    , hoisted
                    , mentionable
                    , managed
                    , permissions
                    , created_at
                    , last_synced
                )
            )
        except Exception as e:
            logger.warning(f"Failed to add role: {role_id} from guild: {id_guild}. Error: {e}")

    def add_member_to_points_table(self, guild_id, member_id, points):
        """

        :param id_guild: The ID of the Guild
        :param id_member: The ID of the Member
        :param points: The amount of points

        """
        query = """INSERT 
                        INTO points
                            (discord_guild_id, discord_member_id, points)
                        VALUES((%s),(%s),(%s))
                            """
        try:
            logger.debug(f"Adding member to points table:{member_id} in {guild_id}")
            self.insert(query,
                        (str(guild_id), str(member_id), 0))
        except Exception as e:
            logger.warning(f"Failed to add member to points table: '{member_id}' in Guild ID: '{guild_id}'."
                           f" Error: {e}")




    # ---------- Update commands
    def update_guild_info(self, g_name, g_logo, g_created_at, g_member_count
                          , g_nsfw_level, g_language, dt_now, guild_id):
        """
        Update guild information in the database.

        Parameters
        ----------
        :param g_name: the name of the guild
        :param g_logo: the logo of the guild
        :param g_created_at: the datetime when the guild was created
        :param g_member_count: the integer of members in the guild
        :param g_nsfw_level: the nsfw level of the guild
        :param g_language: the primary language of the guild
        :param dt_now: the current datetime
        :param guild_id: the id of the discord guild
        """

        query = """UPDATE
                            guilds
                        SET
                            name = (%s)
                          , logo = (%s)
                          , created_at = (%s)
                          , member_count = (%s)
                          , nsfw_level = (%s)
                          , language = (%s)
                          , last_sync = (%s)
                        WHERE
                            discord_guild_id = (%s)"""
        try:
            logger.debug(f"Updating guild: {g_name}, {guild_id}")
            self.update(
                query
                , (g_name
                   , g_logo
                   , g_created_at
                   , g_member_count
                   , g_nsfw_level
                   , g_language
                   , dt_now
                   , str(guild_id))
            )
        except Exception as e:
            logger.warning(f"failed to update guild: {g_name}, {guild_id}. Error: {e}")

    def update_member_info(self, guild_id, member_id, name, avatar, created_at
                           , nickname, display_name, joined_at):
        """
        Updates all member information in the database.

        Parameters
        ----------
        :param guild_id: the id of the discord guild
        :param member_id: the id of the member
        :param name: the name of the member
        :param avatar: the avatar of the member
        :param created_at: the datetime when the member was created
        :param nickname: the nickname of the member
        :param display_name: the display name of the member
        :param joined_at: the datetime when the member joined the guild
        """
        query = """UPDATE 
                            members
                        SET
                            discord_guild_id = (%s)
                            , name = (%s)
                            , avatar = (%s)
                            , created_at = (%s)
                            , nickname = (%s)
                            , display_name = (%s)
                            , joined_at = (%s)
                        WHERE discord_member_id = (%s)
                        """
        try:
            logger.debug(f"Updating member: {name} in guild: {guild_id}")
            self.update(
                query
                , (str(guild_id)
                   , name
                   , avatar
                   , created_at
                   , nickname
                   , display_name
                   , joined_at
                   , str(member_id))
            )
        except Exception as e:
            logger.warning(f"Failed to update member: {name} in guild: {guild_id}. Error: {e}")

    def update_role_in_db(self, id_guild, role_id, role_name, position, color
                          , hoisted, mentionable, managed, permissions, created_at
                          , last_synced):
        """
        Updates all roles in the database.

        Parameters
        ----------
        :param id_guild: the id of the discord guild
        :param role_id: the id of the role
        :param role_name: the name of the role
        :param position: the position of the role in the roles list
        :param color: the color of the role
        :param hoisted: If the role is seperated in the members tab
        :param mentionable: If the role is mentionable or not
        :param managed: If the role is managed or not
        :param permissions: the permissions of the role
        :param created_at: the datetime when the role was created
        :param last_synced: the datetime when the role was last synced
        """
        query = """UPDATE 
                            roles
                        SET
                            discord_guild_id = (%s)
                            , name = (%s)
                            , position = (%s)
                            , color = (%s)
                            , hoisted = (%s)
                            , mentionable = (%s)
                            , managed = (%s)
                            , permissions = (%s)
                            , created_at = (%s)
                            , last_synced = (%s)

                        WHERE role_id = (%s)
                        """
        try:
            logger.debug(f"Updating role: {role_name} in guild: {id_guild}")
            self.update(query, (
                str(id_guild), role_name, position, color, hoisted, mentionable
                , managed, permissions, created_at, last_synced, str(role_id)))
        except Exception as e:
            logger.warning(f"Failed to update role: {role_name} in guild: {id_guild}. Error: {e}")

    def update_channel_in_db(self, guild_id, channel_id, name, category
                             , position, mention, jump_url, permissions_synced
                             , overwrites, created_at, last_synced):
        """
        Updates all channel information for a guild in the database.

        Parameters
        ----------
        :param guild_id: the id of the discord guild
        :param channel_id: the id of the channel
        :param name: the name of the channel
        :param category: the category of the channel
        :param position: the position of the channel in the channels list
        :param mention: If the channel is mentionable or not
        :param jump_url: the jump url of the channel
        :param permissions_synced: the permissions of the channel
        :param overwrites: the overwrites of the channel
        :param created_at: the datetime when the channel was created
        :param last_synced: the datetime when the channel was last synced
        """

        query = """UPDATE 
                            channels
                        SET
                            discord_guild_id = (%s)
                            , channel_name = (%s)
                            , category = (%s)
                            , position = (%s)
                            , mention = (%s)
                            , jump_url = (%s)
                            , permissions_synced = (%s)
                            , overwrites = (%s)
                            , created_at = (%s)
                            , last_synced = (%s)
                        WHERE channel_id = (%s)
                        """
        try:
            logger.debug(f"Updating channel: {name} in guild: {guild_id}")
            self.update(query, (
                str(guild_id), name, category, position, mention, jump_url
                , permissions_synced, overwrites, created_at, last_synced
                , str(channel_id)))
        except Exception as e:
            logger.warning(f"Failed to update channel: {name} in guild: {guild_id}. Error: {e}")

    # ---------- Delete commands
    def delete_guild(self, guild_id):
        """
        removes a guild from the database

        Parameters
        ----------
        :param guild_id: The guild ID
        """
        query = """
                DELETE
                    guilds
                WHERE
                    discord_guild_id = (%s)
                """
        try:
            logger.debug(f"Deleting guild: {guild_id}")
            self.delete(query, (str(guild_id),))
        except Exception as e:
            logger.warning(f"Failed to delete guild: {guild_id}. Error: {e}")

    def delete_member(self, member_id, guild_id):
        """
        Deletes a member from the database.

        Parameters
        ----------
        :param member_id: The member ID
        :param guild_id: The guild ID
        """
        query = """
                DELETE FROM
                    members
                WHERE
                    discord_member_id = (%s) 
                    and discord_guild_id = (%s)
                """
        try:
            logger.debug(f"Deleting member: {member_id} from guild: {guild_id}")
            self.delete(query, (member_id, str(guild_id),))
        except Exception as e:
            logger.warning(f"Failed to delete member: {member_id} from guild: {guild_id}. Error: {e}")

    def delete_role(self, role_id, guild_id):
        """
        Deletes a role from the database.

        Parameters
        ----------
        :param role_id: The role ID
        :param guild_id: The guild ID
        """
        query = """
                DELETE FROM
                    roles
                WHERE
                    role_id = (%s) 
                    and discord_guild_id = (%s)
                """
        try:
            logger.debug(f"Deleting role: {role_id} in guild: {guild_id}")
            self.delete(query, (role_id, str(guild_id),))
        except Exception as e:
            logger.warning(f"Failed to delete role: {role_id} from guild: {guild_id}. Error: {e}")

    def delete_channel(self, channel_id, guild_id):
        """
        Deletes a channel from the database.

        Parameters
        ----------
        :param channel_id: The channel ID
        :param guild_id: The guild ID
        """
        query = """
                DELETE FROM
                    channels
                WHERE
                    channel_id = (%s) 
                    and discord_guild_id = (%s)
                """
        try:
            logger.debug(f"Deleting channel: {channel_id} in guild: {guild_id}")
            self.delete(query, (channel_id, str(guild_id),))
        except Exception as e:
            logger.warning(f"Failed to delete channel: {channel_id} from guild: {guild_id}. Error: {e}")

    def delete_member_from_points_table(self, guild_id, member_id):
        """

        :param id_guild: The ID of the Guild
        :param id_member: The ID of the Member
        """
        query = """
                    DELETE FROM
                        points
                    WHERE
                        discord_member_id = (%s)
                        AND discord_guild_id = (%s)
                """
        try:
            logger.debug(f"Removing member from points table:{member_id} in {guild_id}")
            self.delete(query,
                        (str(guild_id), str(member_id)))
        except Exception as e:
            logger.warning(f"Failed to remove member from points table: '{member_id}' in Guild ID: '{guild_id}'."
                           f" Error: {e}")

    """
    4th Layer. 
    From here we create:
    - Database Syncs
    - Database Jobs
    - Any background database tasks

    """

    def sync(self, guilds=True, channels=True, members=True, roles=True, settings=True):
        """
        Allows us to sync the database with all discord server information.
        This can be a new server, or an existing server in the DB.

        :param guilds: boolean indicating if we want to sync guilds
        :param channels: boolean indicating if we want to sync channels
        :param members: boolean indicating if we want to sync member information
        :param roles: boolean indicating if we want to sync role information
        :param settings: boolean indicating if we want to sync settings information
        """

        def sync_guild_info():
            """
            Syncs all guild information in the database.
            If the guild is not in the database, it will be added.
            If the guild is in the database, it will be updated.

            """
            logger.info("Starting database sync...")

            for guild in self.discord_client.guilds:
                logger.info("Syncing guild...")
                if self.is_guild_in_db(guild.id) is None:
                    self.add_guild_to_guilds_table(
                        guild.name
                        , str(guild.icon)
                        , guild.created_at
                        , guild.member_count
                        , guild.nsfw_level[0]
                        , guild.preferred_locale[1]
                        , guild.id
                        , False
                        , False
                        , datetime.now()
                    )
                else:
                    self.update_guild_info(
                        guild.name
                        , str(guild.icon)
                        , guild.created_at
                        , guild.member_count
                        , guild.nsfw_level[0]
                        , guild.preferred_locale[1]
                        , datetime.now()
                        , guild.id
                    )

        def sync_channel_info():
            """
            Syncs all channel information in the database.
            If the channel does not exist in the database, it will be added.
            If the channel exists in the database, it will be updated.

            """
            for guild in self.discord_client.guilds:
                logger.info("Syncing channel...")
                for channel in guild.channels:
                    if self.is_channel_in_db(channel.id) is None:
                        self.add_channel_to_channel_table(
                            channel.guild.id
                            , channel.id
                            , channel.name
                            , 'Category' if channel.category is None else str(channel.category)
                            , channel.position
                            , channel.mention
                            , channel.jump_url
                            , channel.permissions_synced
                            , str(channel.overwrites)
                            , channel.created_at
                            , datetime.now()
                        )
                    else:
                        self.update_channel_in_db(
                            channel.guild.id
                            , channel.id
                            , channel.name
                            , 'Category' if channel.category is None else str(channel.category)
                            , channel.position
                            , channel.mention
                            , channel.jump_url
                            , channel.permissions_synced
                            , str(channel.overwrites)
                            , channel.created_at
                            , datetime.now()
                        )

        def sync_role_info():
            """
            Syncs all role information in the database.
            If the role does not exist in the database, it will be added.
            If the role exists in the database, it will be updated.

            """
            for guild in self.discord_client.guilds:
                logger.info("Syncing roles...")
                for role in guild.roles:
                    if self.is_role_in_db(role.id) is None:
                        self.add_role_to_roles_table(
                            str(role.guild.id)
                            , str(role.id)
                            , role.name
                            , role.position
                            , str(role.color)
                            , role.hoist
                            , role.mentionable
                            , role.managed
                            , str(role.permissions)
                            , role.created_at
                            , datetime.now()
                        )
                    else:
                        self.update_role_in_db(
                            str(role.guild.id)
                            , str(role.id)
                            , role.name
                            , role.position
                            , str(role.color)
                            , role.hoist
                            , role.mentionable
                            , role.managed
                            , str(role.permissions)
                            , role.created_at
                            , datetime.now()
                        )

        def sync_member_info():
            """
            Syncs all member information in the database.
            If the member does not exist in the database, it will be added.
            If the member exists in the database, it will be updated.

            """
            for guild in self.discord_client.guilds:
                logger.info("Syncing members...")
                for member in guild.members:
                    if self.is_member_in_db(member.id) is None:
                        self.add_member_to_members_table(
                            member.guild.id
                            , member.id
                            , member.name
                            , str(member.avatar)
                            , member.nick
                            , member.display_name
                            , member.top_role
                            , member.created_at
                            , member.joined_at
                            , datetime.now()
                        )
                    else:
                        self.update_member_info(
                            member.guild.id
                            , member.id
                            , member.name
                            , str(member.avatar)
                            , member.created_at
                            , member.nick
                            , member.display_name
                            , member.joined_at
                        )

        def sync_settings_info():
            """
            Created an entry in the settings table for a new guild.
            Existing guilds are not modified

            """
            for guild in self.discord_client.guilds:
                logger.info("Adding settings...")
                if not self.is_settings_in_db(guild.id):
                    self.add_settings_to_bot_settings_table(
                        guild.id
                        , self.discord_client.user.id
                        , True
                        , True
                        , True
                        , True
                        , True
                        , datetime.now()
                    )

        if guilds:
            sync_guild_info()

        if channels:
            sync_channel_info()

        if roles:
            sync_role_info()

        if members:
            sync_member_info()

        if settings:
            sync_settings_info()

    """
    5th layer.
    Here we handle specific logic for certain features.
    
    """

    # POINTS
    def get_points(self, member):
        select_query = """
                        SELECT
                            points 
                        FROM
                            points
                        WHERE
                            discord_member_id = (%s)
                        """
        return self.select_one(select_query, member.id)

    def add_points(self, member, amount):
        select_query = """
                        SELECT
                            points 
                        FROM
                            points
                        WHERE
                            discord_member_id = (%s)
                        """
        update_query = """UPDATE 
                            points
                        SET
                            points = (%s)
                        WHERE discord_member_id = (%s)
                        """
        try:
            current_points = self.select_one(select_query, member.id)
            new_points = current_points + amount

            logger.debug(f"Adding {new_points} to {member.name} in guild: {member.guild.id}")
            self.update(update_query, (new_points, member.id))

        except Exception as e:
            logger.warning(f"Failed to add points for: {member.name} in guild: {member.guild.id}. Error: {e}")

    def remove_points(self, member, amount):
        select_query = """
                        SELECT
                            points 
                        FROM
                            points
                        WHERE
                            discord_member_id = (%s)
                        """
        update_query = """
                        UPDATE 
                            points
                        SET
                            points = (%s)
                        WHERE
                            discord_member_id = (%s)
                        """
        try:
            current_points = self.select_one(select_query, member.id)
            new_points = current_points - amount

            logger.debug(f"Removing {new_points} to {member.name} in guild: {member.guild.id}")
            self.update(update_query, (new_points, member.id))

        except Exception as e:
            logger.warning(f"Failed to remove points for: {member.name} in guild: {member.guild.id}. Error: {e}")


def init_db(bot: Bot):
    # This is called in the main bot file and is the bit of code that connects to the database.
    db_client = DB(bot)
    bot.db = db_client
