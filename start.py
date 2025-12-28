import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = 'Вставить свой токен'

JOIN_GAME_BUTTON_TEXT = 'Присоединиться к игре'
START_COMMAND = 'start'
JOIN_CALLBACK_DATA = 'join'
GREETING_TEXT = 'Добро пожаловать! Нажмите кнопку для добавления в игру.'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=[START_COMMAND])
def start_game_message(message):
    chat = get_chat_from_message(message)
    chat_id = get_chat_id(chat)
    keyboard = create_keyboard_start_game()
    send_message(chat_id, GREETING_TEXT, keyboard)
    
def get_chat_from_message(message):
    return message.chat

def get_chat_id(chat):
    return chat.id

def create_keyboard_start_game():
    keyboard = types.InlineKeyboardMarkup()
    join_button = types.InlineKeyboardButton(JOIN_GAME_BUTTON_TEXT, callback_data=JOIN_CALLBACK_DATA)
    keyboard.add(join_button)
    return keyboard

def send_message(chat_id, message, reply_markup=None):
        return bot.send_message(chat_id, message, reply_markup=reply_markup)