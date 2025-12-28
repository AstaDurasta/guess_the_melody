from start import *
from build import *

BUTTON_START_GAME = 'Готов играть'
BUTTON_EXIT_GAME = 'Выйти из игры'
GAME_STATUS_ALREADY_PLAYING = "Ты уже в игре"

PLAY_CALLBACK_COMAND = 'play'
EXIT_CALLBACK_COMAND = 'exit'

COUNT_ROWS_QUERY = 'COUNT(*)'
INDEX_OF_FIRST_RESULT = 0
FIRST_COLUMN_INDEX = 0
USER_ABSENCE = 0

database = initialization()


@bot.callback_query_handler(func=lambda call: call.data == JOIN_CALLBACK_DATA)
def register_new_player(call):
    chat = get_chat_from_call(call)
    chat_id = get_chat_id(chat)
    user_id = get_user_id(call)
    if validate_user_existence(user_id):
        send_message(chat_id, GAME_STATUS_ALREADY_PLAYING)
    else:
        player_name = get_username(call)
        message_text = get_player_registration_message(player_name)
        keyboard = create_game_keyboard()
        add_player(chat_id, user_id)
        send_message(chat_id, message_text, keyboard)
    answer_callback(call)

def get_chat_from_call(call):
    return call.message.chat

def get_username(call):
    return call.from_user.first_name

def get_player_registration_message(player_name):
    return f'Ура! У нас новый игрок — {player_name}!'

def create_game_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    play_button = types.InlineKeyboardButton(BUTTON_START_GAME, callback_data=PLAY_CALLBACK_COMAND)
    exit_button = types.InlineKeyboardButton(BUTTON_EXIT_GAME, callback_data=EXIT_CALLBACK_COMAND)
    keyboard.add(play_button,  exit_button)
    return keyboard

def get_user_id(call):
    return call.from_user.id

def add_player(chat_id, user_id):
    fields = get_user_table_insert_fields()
    values = get_user_table_insert_values(user_id, chat_id)
    insert_row(USERS_TABLE_NAME, fields, values)

def get_user_table_insert_fields():
    return 'user_id, chat_id'

def get_user_table_insert_values(user_id, chat_id):
    return f"{user_id}, {chat_id}"

def insert_row(table_name, fields, values):
    database.add_row_to_table(table_name, fields, values)

def validate_user_existence(user_id):
    condition = get_user_condition(user_id)
    sample = select(USERS_TABLE_NAME, COUNT_ROWS_QUERY, condition)
    user_found = sample[INDEX_OF_FIRST_RESULT][FIRST_COLUMN_INDEX] > USER_ABSENCE
    return user_found

def get_user_condition(user_id):
    return f'user_id={user_id}'

def select(table_name, fields, condition=None):
    return database.select(table_name, fields, condition)

def answer_callback(call):
    call_id = get_call_id(call)
    bot.answer_callback_query(call_id)

def get_call_id(call):
    return call.id

def answer_callback_query(call_id):
    bot.answer_callback_query(call_id)