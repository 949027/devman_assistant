from dotenv import load_dotenv
from django.core.management.base import BaseCommand
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
json_blank = {}        # Записать в базу


time_keyboard = [['18:00-18:30', '18:30-19:00', '19:00-19:30', '19:30-20:00', 'Любое время', 'Ни один не подходит']]
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
    student_id = update.effective_message.from_user.username
    last_student_time = json_blank[student_id]
    context.bot.send_message(
        chat_id=chat_id,
        text=f'Вы уже указывали время созвона - {last_student_time}.\n'
             'Если вы хотите изменить его, выберите соответствующий пункт меню.',
        reply_markup = ReplyKeyboardMarkup(new_blank_keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    return 'CHOICE_CHECK'


def choice_check(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    user_reply = update.effective_message.text
    if user_reply == 'Изменить время':
        context.bot.send_message(
            chat_id=chat_id,
            text= ' Выберите удобный для вас интервал созвона из списка',
            reply_markup = ReplyKeyboardMarkup(time_keyboard, resize_keyboard=True, one_time_keyboard=True) 
        )
        return 'TIME'
    elif user_reply == 'Выйти':
        context.bot.send_message(
            chat_id=chat_id,
            text='Вы вышли из процедуры изменения времени созвона\n'
                 'если вы всё-таки хотите поменять, напишите /start'
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text='Я вас не понимаю, если хотите начать заново, напишите /start'
        )


def get_student_time(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    student_username = update.effective_message.from_user.username
    student_reply = update.effective_message.text
    if student_reply == 'Любое время':
        context.bot.send_message(
            chat_id=chat_id,
            text='Вы выбрали любое время созвона. Когда группы будут распределены, конкретное время вам сообщит куратор'
        )
        student_blank.update({'Время': student_reply})
        json_blank.update({student_username: student_reply})
    else:    
        context.bot.send_message(
            chat_id=chat_id,
            text = f'Вы выбрали созвон, который начинается в {student_reply}\n'
        )
        student_blank.update({'Время': student_reply})
        json_blank.update({student_username: student_reply})

    with open('student_blank.json', 'w', encoding='utf-8') as file:
        json.dump(json_blank, file, ensure_ascii=False)
    
    student_blank.clear()
    
   
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
            user_state = 'NEW_BLANK'
        else:     
            user_state = 'START'
    else:
        user_state = states_database.get(chat_id)

    states_functions = {
        'START': start,
        'TIME': get_student_time,
        'NEW_BLANK': make_new_blank,
        'CHOICE_CHECK': choice_check
    }

    state_handler = states_functions[user_state]
    next_state = state_handler(update, context)
    states_database.update({chat_id: next_state})


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_dotenv()
        telegram_token= os.getenv('TELEGRAM_BOT_TOKEN')
        updater = Updater(telegram_token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', handle_user_reply))
        dispatcher.add_handler(MessageHandler(Filters.text, handle_user_reply))
        dispatcher.add_handler(CallbackQueryHandler(handle_user_reply))
        updater.start_polling()