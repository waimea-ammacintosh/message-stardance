#============================================================================
# Database schema and seed data configuration
#============================================================================


#----------------------------------------------------------------------------
# Table definitions
#----------------------------------------------------------------------------
# Define your tables with a name, a schema and optional seed/sample data,
# using this format, and then add the tables to the Table Registry below:
#
# class TableName:
#     NAME      = "name"
#     SCHEMA    = "CREATE TABLE name (...)"
#     SEED_DATA = "INSERT INTO name (...)" or None
#----------------------------------------------------------------------------

class UserTable:

    NAME = "users"

    SCHEMA = """
        CREATE TABLE users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            forename  TEXT NOT NULL,
            lastname  TEXT NOT NULL,
            username  TEXT NOT NULL,
            email     TEXT NOT NULL,
            pw_hash   TEXT NOT NULL,
            icon_file TEXT NOT NULL,
            admin     BOOLEAN NOT NULL
        )
    """

    SEED_DATA = """
        INSERT INTO users ('admin', 'admin', 'admin', )
    """

# Add more table classes here...
class MessageTable:

    NAME = "messages"

    SCHEMA = """
        CREATE TABLE messages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            message     TEXT NOT NULL,
            sender_id   INTEGER NOT NULL,
            reciever_id INTEGER NOT NULL,

            FOREIGN KEY(sender_id) references (users.id)
            FOREIGN KEY(reciever_id) references (users.id)
        )
    """

    SEED_DATA = """
    """



#----------------------------------------------------------------------------
# Table registry
#----------------------------------------------------------------------------
# Register all of your tables by adding them to the TABLES list here:
#
# TABLES = [
#     Table1,
#     Table2,
#     etc.
# ]
#
# Note: The table order is important - Create the tables that have
#       foreign keys AFTER the tables they link to have been created
#----------------------------------------------------------------------------

TABLES = [
    UserTable,
    MessageTable,
    # Add more tables here...
]

