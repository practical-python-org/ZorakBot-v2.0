DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'zorak_db') THEN
        CREATE DATABASE zorak_db;
    END IF;
END $$;

DO $$
    BEGIN
    ----------------------------------------------------------------
    -- GUILDS
    ----------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'guilds') THEN
        -- Create the table
        CREATE TABLE guilds (
            id SERIAL PRIMARY KEY,
            discord_guild_id TEXT,
            name TEXT,
            logo TEXT,
            member_count INT,
            language TEXT,
            nsfw_level TEXT,
            is_premium BOOL,
            is_test BOOL,
            created_at TIMESTAMP,
            last_sync TIMESTAMP
        );
    END IF;

    ----------------------------------------------------------------
    -- MEMBERS
    ----------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'members') THEN
        -- Create the table
        CREATE TABLE members (
            id SERIAL PRIMARY KEY,
            discord_guild_id TEXT,
            discord_member_id TEXT,
            name TEXT,
            avatar TEXT,
            nickname TEXT,
            display_name TEXT,
            top_role TEXT,
            joined_at TIMESTAMP,
            created_at TIMESTAMP,
            last_sync TIMESTAMP
            -- FOREIGN KEY (discord_guild_id) REFERENCES guilds(discord_guild_id)
        );
    END IF;

    ----------------------------------------------------------------
    -- CHANNELS
    ----------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'channels') THEN
        -- Create the channels table
        CREATE TABLE channels (
            id SERIAL PRIMARY KEY,
            discord_guild_id TEXT,
            channel_id TEXT,
            channel_name TEXT,
            category TEXT,
            position INT,
            mention TEXT,
            jump_url TEXT,
            permissions_synced BOOL,
            overwrites TEXT,
            created_at TIMESTAMP,
            last_synced TIMESTAMP
            -- FOREIGN KEY (discord_guild_id) REFERENCES guilds(discord_guild_id)
        );
    END IF;


    ----------------------------------------------------------------
    -- CHANNEL_SETTINGS
    ----------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'channel_settings') THEN
        -- Create the channel_settings table
        CREATE TABLE channel_settings (
            id SERIAL PRIMARY KEY,
            discord_guild_id TEXT,
            channel_id TEXT,
            join_log BOOL,
            chat_log BOOL,
            moderation_log BOOL,
            server_log BOOL
            --FOREIGN KEY (discord_guild_id) REFERENCES guilds(discord_guild_id),
            --FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
        );
    END IF;


    ----------------------------------------------------------------
    -- ROLES
    ----------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'roles') THEN
        -- Create the roles table
        CREATE TABLE roles (
            id SERIAL PRIMARY KEY,
            discord_guild_id TEXT,
            role_id TEXT,
            name TEXT,
            position INT,
            color TEXT,
            hoisted BOOL,
            mentionable BOOL,
            managed BOOL,
            permissions TEXT,
            created_at TIMESTAMP,
            last_synced TIMESTAMP
            -- FOREIGN KEY (discord_guild_id) REFERENCES guilds(discord_guild_id)
        );
    END IF;

    ----------------------------------------------------------------
    -- POINTS
    ----------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'points') THEN
        -- Create the points table
        CREATE TABLE points (
            id SERIAL PRIMARY KEY,
            discord_guild_id TEXT,
            discord_member_id TEXT,
            points INT
            --FOREIGN KEY (discord_guild_id) REFERENCES guilds(discord_guild_id),
            --FOREIGN KEY (discord_member_id) REFERENCES members(discord_member_id)
        );
    END IF;

    ----------------------------------------------------------------
    -- BOT_SETTINGS
    ----------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'bot_settings') THEN
        -- Create the bot_settings table
        CREATE TABLE bot_settings (
            id SERIAL PRIMARY KEY,
            discord_guild_id TEXT,
            discord_bot_id TEXT,
            admin BOOL,
            moderation BOOL,
            logging BOOL,
            antispam BOOL,
            fun BOOL,
            last_sync TIMESTAMP
            --FOREIGN KEY (discord_guild_id) REFERENCES guilds(discord_guild_id)
        );
    END IF;

    ----------------------------------------------------------------
    -- MODERATION
    ----------------------------------------------------------------
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'moderation') THEN
        -- Create the moderation table
        CREATE TABLE moderation (
            id SERIAL PRIMARY KEY,
            discord_guild_id TEXT,
            discord_member_id TEXT,
            reason TEXT,
            note TEXT,
            warning BOOL
            --FOREIGN KEY (discord_guild_id) REFERENCES guilds(discord_guild_id),
            --FOREIGN KEY (discord_member_id) REFERENCES members(discord_member_id)
        );
    END IF;
END $$;