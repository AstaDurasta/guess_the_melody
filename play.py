from exit import *
import random


SOUND_SELECT_COLUMNS = 'id, sound_name'
MAX_INCORRECT_ANSWERS = 3
CALLBACK_COMAND_FAILED = 'failed'
CALLBACK_COMAND_GUASSED = 'guessed'

FIRST_BUTTON = 0
SECOND_BUTTON = 1
THIRD_BUTTON = 2
FOURTH_BUTTON = 3

MUSIC_DIRECTORY = 'sounds/'
BINARY_READ_MODE = 'rb'

SCORE_INCREMENT = 1
TABLE_HEADER_NAMES = 'Игрок     |     Счет\n'


@bot.callback_query_handler(func=lambda call: call.data == PLAY_CALLBACK_COMAND)
def handle_callback_command_play(call):
    activate_player(call)
    if are_all_players_ready(call):
        send_random_song_with_choices(call)
         
def activate_player(call):
    user_id = get_user_id(call)
    user_id_condition = f'user_id={user_id}'
    user_status = 'status=TRUE'
    update_user_table(user_id_condition, user_status)

def update_user_table(condition, update):
    database.update_table(USERS_TABLE_NAME, update, condition)

def are_all_players_ready(call):
    chat_id = get_chat_id_from_call(call)
    unready_player_count = count_unready_players(chat_id)
    return unready_player_count == 0

def get_chat_id_from_call(call):
    chat = get_chat_from_call(call)
    return get_chat_id(chat)

def get_chat_from_call(call):
    chat = call.message.chat
    return chat

def count_unready_players(chat_id):
    condition = get_unready_players_filter(chat_id)
    sample = select(USERS_TABLE_NAME, COUNT_ROWS_QUERY, condition)
    unready_player_count = sample[INDEX_OF_FIRST_RESULT][FIRST_COLUMN_INDEX]
    return unready_player_count

def get_unready_players_filter(chat_id):
    return f"status=0 and chat_id={chat_id}"

def send_random_song_with_choices(call):
    chat_id = get_chat_id_from_call(call)
    audio_file_to_play, sound_name = get_music_file_info()
    keyboard = create_song_choice_keyboard(sound_name)
    audiofile = get_audiofile(audio_file_to_play)
    send_music(chat_id, audiofile, keyboard)
    answer_callback(call)
    

def get_music_file_info():
    songs = get_all_sound_info()
    random_song = get_random_song(songs)
    return random_song

def get_all_sound_info(condition=None):
    rows = select(SOUNDS_TABLE_NAME, SOUND_SELECT_COLUMNS, condition)
    sounds = []
    for file_name, sound_name in rows:
        sounds.append((file_name, sound_name))
    return sounds

def get_random_song(songs):
    return random.choice(songs)

def create_song_choice_keyboard(sound_name):
    four_answer_options = get_four_answer_options(sound_name)
    keyboard = create_song_selection_keyboard(four_answer_options)
    return keyboard
    
    
def get_four_answer_options(selected_song):
    condition = get_sound_exclusion_condition(selected_song)
    all_songs = get_all_sound_info(condition)
    shuffle(all_songs)
    three_random_songs = get_three_titles(all_songs)
    four_answer_options = prepare_four_answer_options(three_random_songs, selected_song)
    return four_answer_options
    
def get_sound_exclusion_condition(selected_song):
    return f'sound_name!="{selected_song}"'

def shuffle(songs):
    random.shuffle(songs)

def get_three_titles(songs):
    first_three_songs = songs[:MAX_INCORRECT_ANSWERS]
    three_songs = []
    for id, song_title in first_three_songs:
        three_songs.append((song_title, CALLBACK_COMAND_FAILED))
    return three_songs

def prepare_four_answer_options(three_random_songs, selected_song):
    four_answer_options = three_random_songs
    four_answer_options.append((selected_song, CALLBACK_COMAND_GUASSED))
    shuffle(four_answer_options)
    return four_answer_options

def create_song_selection_keyboard(song_titles):
    keyboard = get_keyboard()
    song_selection_keyboard = add_buttons_to_keyboard(song_titles, keyboard)
    return song_selection_keyboard

def get_keyboard():
    return types.InlineKeyboardMarkup()

def add_buttons_to_keyboard(song_titles, keyboard):
    buttons = []
    for song_title, song_status in song_titles:
        button = get_button(song_title, song_status)
        buttons.append(button)
    keyboard.add(buttons[FIRST_BUTTON], buttons[SECOND_BUTTON])
    keyboard.add(buttons[THIRD_BUTTON], buttons[FOURTH_BUTTON])
    return keyboard

def get_button(song_title, song_status):
    return types.InlineKeyboardButton(text=song_title, callback_data=song_status)

def get_audiofile(filename):
    file_path = get_file_path(filename)
    audio_file = load_audio_file(file_path)
    return audio_file

def get_file_path(filename):
    return f'{MUSIC_DIRECTORY}{filename}.mp3'

def load_audio_file(filename):
    audio_file = open(filename, BINARY_READ_MODE)
    return audio_file

def send_music(chat_id, audiofile, reply_markup=None):
    return bot.send_audio(chat_id=chat_id, audio=audiofile, reply_markup=reply_markup)

@bot.callback_query_handler(func=lambda call: call.data == CALLBACK_COMAND_FAILED)
def send_wrong_answer_notification(call):
    chat_id = get_chat_id_from_call(call)
    player_name = get_username(call)
    message = generate_wrong_answer_message(player_name)
    send_message(chat_id, message)
    answer_callback(call)

def generate_wrong_answer_message(player_name):
    return f"{player_name} ответил неверно! 🙄"

@bot.callback_query_handler(func=lambda call: call.data == CALLBACK_COMAND_GUASSED)
def finish_game(call):
    complete_game(call)
    announce_winner(call)
    show_leaderboard(call)

def complete_game(call):
    chat_id = get_chat_id_from_call(call)
    message_id = get_message_id(call)
    delete_keyboard(chat_id, message_id)
    reset_all_user_statuses(chat_id)

def get_message_id(call):
    return call.message.message_id

def delete_keyboard(chat_id, message_id):
    bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)

def reset_all_user_statuses(chat_id):
    condition = f'chat_id={chat_id}'
    update = 'status=FALSE'
    database.update_table(USERS_TABLE_NAME, update, condition)

def announce_winner(call):
    user_id = get_user_id(call)
    player_name = get_username(call)
    increase_score_winner(user_id)
    chat_id = get_chat_id_from_call(call)
    message = get_winner_announcement(player_name)
    send_message(chat_id, message)

def increase_score_winner(user_id):
    new_score_winner = get_new_score_winner(user_id)
    update_winner_score(user_id, new_score_winner)

def get_new_score_winner(user_id):
    current_winner_score = get_player_score(user_id)
    updated_winner_score  = current_winner_score + SCORE_INCREMENT
    return updated_winner_score

def get_player_score(user_id):
    fields = "score"
    condition = f"user_id={user_id}"
    sample = database.select(USERS_TABLE_NAME, fields, condition)
    return sample[INDEX_OF_FIRST_RESULT][FIRST_COLUMN_INDEX]

def update_winner_score(user_id, new_score):
    updates = f"score={new_score}"
    condition = f"user_id={user_id}"
    database.update_table(USERS_TABLE_NAME, updates, condition)

def get_winner_announcement(player_name):
    return f"Победил {player_name}!!! 🎉"

def show_leaderboard(call):
    chat_id = get_chat_id_from_call(call)
    leaderboard = format_leaderboard(chat_id)
    keyboard = create_game_keyboard()
    send_message(chat_id, leaderboard, keyboard)
    

def format_leaderboard(chat_id):
    players = get_all_users(chat_id)
    leaderboard =  build_leaderboard(players)
    return leaderboard

def get_all_users(chat_id):
    fields = 'user_id, score'
    condition=f'chat_id={chat_id}'
    players = database.select(USERS_TABLE_NAME, fields, condition) 
    return players

def build_leaderboard(players):
    table_rows = [TABLE_HEADER_NAMES]
    for user_id, score in players:
        leaderboard_row = create_leaderboard_row(user_id, score)
        table_rows.append(leaderboard_row)
    leaderboard = ''.join(table_rows)
    return leaderboard

def create_leaderboard_row(user_id, score):
    user_name = get_username_by_id(user_id)
    return f'{user_name}     |     {score}\n'

def get_username_by_id(user_id):
    chat_full_info = get_chat_information(user_id)
    username = get_username_from_chat(chat_full_info)
    return username

def get_chat_information(user_id):
    return bot.get_chat(chat_id=user_id)

def get_username_from_chat(chat_info):
    return chat_info.first_name