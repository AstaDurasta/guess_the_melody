from add import *

EXIT_GAME_MESSAGE = 'Вы вышли из игры.'

@bot.callback_query_handler(func=lambda call: call.data == EXIT_CALLBACK_COMAND)
def exit_game(call):
    chat = get_chat_from_call(call)
    chat_id = get_chat_id(chat)
    user_id = get_user_id(call)
    delete_player(user_id)
    send_message(chat_id, EXIT_GAME_MESSAGE)
    answer_callback(call)

def delete_player(user_id):
    condition = get_user_condition(user_id)
    delete_rows(condition)

def delete_rows(condition):
    database.delete_rows(USERS_TABLE_NAME, condition)