from database import Database

USERS_TABLE_NAME = "users"
USERS_TABLE_FIELDS = 'user_id INT PRIMARY KEY, chat_id INT, score INT DEFAULT 0, status BOOLEAN DEFAULT FALSE'

SOUNDS_TABLE_NAME = "sounds"
SOUNDS_TABLE_FIELDS = 'id INTEGER PRIMARY KEY AUTOINCREMENT, sound_name TEXT NOT NULL'

def initialization():
    database = Database("database.db") 
    database.create_table(USERS_TABLE_NAME, USERS_TABLE_FIELDS)
    database.create_table(SOUNDS_TABLE_NAME, SOUNDS_TABLE_FIELDS)
    return database