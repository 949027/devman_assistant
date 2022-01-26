from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Filters
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
import json


states_database = {}
student_blank = {}
json_blank = {}         # Записать в базу


time_keyboard = [['18:00-18:30', '18:30-19:00', '19:00-19:30', '19:30-20:00', 'Ни один не подходит']]
new_blank_keyboard = [['Изменить время','Выйти']]


def start(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    context.bot.send_message(
        chat_id=chat_id,
        text=' Привет, я бот, созданный для упрощения работы по организации проектов для курсов Devman.'
             ' Выберите удобный для вас интервал созвона из списка',
        reply_markup = ReplyKeyboardMarkup(time_keyboard, resize_keyboard=True, one_time_keyboard=True) 
    )
    
    return 'TIME'


def make_new_blank(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    context.bot.send_message(
        chat_id=chat_id,
        text=' Выберите удобный для вас интервал созвона из списка',
        reply_markup = ReplyKeyboardMarkup(time_keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return 'TIME'
     

def get_student_time(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    student_time = update.effective_message.text
    student_username = update.effective_message.from_user.username
    context.bot.send_message(
        chat_id=chat_id,
        text = f'Вы выбрали созвон, который начинается в {student_time}\n'
    )
    student_blank.update({'Время': student_time})
    json_blank.update({student_username: student_time})

    with open('student_blank.json', 'w', encoding='utf-8') as file:
        json.dump(json_blank, file, ensure_ascii=False)
    
    student_blank.clear()

    return 'SKILL'
    
   
def handle_user_reply(update: Update, context: CallbackContext):
    with open('student_blank.json', 'r', encoding='utf-8') as file:
        json_student_blank = json.load(file)
        json_blank.update(json_student_blank)

    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
        user_id = update.message.from_user.id
        username = update.message.from_user.username

    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return

    if user_reply == '/start':
        if username in json_student_blank:
            context.bot.send_message(
                chat_id=chat_id,
                text = 'Вы уже выбрали время созвона, если хотите внести изменения, напишите куратору'
            )
        else:     
            user_state = 'START'
    else:
        user_state = states_database.get(chat_id)

    states_functions = {
        'START': start,
        'TIME': get_student_time,
        'NEW_BLANK': make_new_blank,
    }

    state_handler = states_functions[user_state]
    next_state = state_handler(update, context)
    states_database.update({chat_id: next_state})


def main():
    load_dotenv()
    telegram_token= os.getenv('TELEGRAM_BOT_TOKEN')
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', handle_user_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_user_reply))
    dispatcher.add_handler(CallbackQueryHandler(handle_user_reply))
    updater.start_polling()

if __name__=='__main__':
    main()