import os
from join import *

ADD_COMAND = 'add'
CONTENT_TYPE_AUDIO = 'audio'
SOUND_NAME_COLUMN = 'sound_name'
SOUNDS_DIRECTORY = "sounds"
BINARY_WRITE_MODE = 'wb'

@bot.message_handler(commands=[ADD_COMAND])
def handle_add_command(message):
    chat = get_chat_from_message(message)
    chat_id = get_chat_id(chat)
    username = get_username(message)
    text_message = format_sound_request_text(username)
    sent_message = send_message(chat_id, text_message)
    add_next_step_handler(sent_message, handle_audio_message)

def format_sound_request_text(username):
    return f'{username}, пожалуйста, отправь музыкальный файл с правильным названием файла.'

def add_next_step_handler(message, func):
    bot.register_next_step_handler(message, func)

def handle_audio_message(message):
    if validate_audio_message(message):
        sound_name = get_sound_name(message)
        add_new_melody(sound_name)
        download_file(message)
        message_text = create_upload_notification(sound_name)
    else:
        message_text = create_upload_notification()
    chat = get_chat_from_message(message)
    chat_id = get_chat_id(chat)
    send_message(chat_id, message_text)

def validate_audio_message(message):
    return message.content_type == CONTENT_TYPE_AUDIO

def get_sound_name(message):
    sound_name = message.audio.file_name
    return f'"{sound_name}"'

def add_new_melody(melody_name):
    database.add_row_to_table(SOUNDS_TABLE_NAME, SOUND_NAME_COLUMN, melody_name)

def download_file(message):
    file_id = get_file_id(message)
    file_path = get_file_path(file_id)
    downloaded_file = download_file_content(file_path)
    save_downloaded_audio_file(downloaded_file)

def get_file_id(message):
    return message.audio.file_id

def get_file_path(file_id):
    file = bot.get_file(file_id)
    file_path = file.file_path
    return file_path

def download_file_content(file_path):
    return bot.download_file(file_path)

def save_downloaded_audio_file(download_file):
    new_file_name = generate_new_file_name()
    file_path = create_file_path(new_file_name)
    save_sound_file(file_path, download_file)

def generate_new_file_name():
    file_id = database.get_max_id(SOUNDS_TABLE_NAME)
    file_name = f'{file_id}.mp3'
    return file_name

def create_file_path(file_name):
    return os.path.join(SOUNDS_DIRECTORY, file_name)

def save_sound_file(file_path, sound_file_data):
    with open(file_path, BINARY_WRITE_MODE) as sound_file:
        sound_file.write(sound_file_data)

def create_upload_notification(sound_name=None):
    if sound_name:
        message = f"Звук '{sound_name}' успешно добавлен в базу данных!"
    else:
        message = "Пожалуйста, отправьте именно музыкальный файл."
    return message