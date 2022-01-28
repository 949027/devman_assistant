import os
from dotenv import load_dotenv

import telegram
from telegram import Update
from telegram.ext import Updater
from telegram.ext import Dispatcher
from telegram.ext import Filters
from telegram.ext import CommandHandler,MessageHandler
from telegram.ext import CallbackContext
from telegram import ReplyKeyboardMarkup
import json
from django.core.management.base import BaseCommand

states_database = {}
student_blank ={}
json_blank = {}


accept_decline_keyboard =[['Согласен', 'Не подходит']]


def last_time_inform(bot):
    with open('groups_time.json','r',encoding='utf-8') as file:
        groups = json.load(file)

    for group in groups:
        some_group = groups[group]
    if len(some_group['students'])<3:
        group_time = some_group['time'] 
        bot.send_message(
            chat_id='619160718',
            text=f'{group}, время созвона {group_time}',
            reply_markup=ReplyKeyboardMarkup(accept_decline_keyboard,resize_keyboard=True,one_time_keyboard=True)
        )
        student_blank.update({'Время': group_time})
    elif len(some_group['students'])>=3:
        bot.send_message(
            chat_id='619160718',
            text='Вам нужно будет записаться на следующую неделю.'
        )
    
    
def student_positive_choice(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    student_reply = update.effective_message.text
    student_username = update.effective_message.from_user.username
    if student_reply == 'Согласен':
        context.bot.send_message(
            chat_id=chat_id,
            text='Мы записали вас на проект на ближней недели, ПМ вас добавит в группу в телеграме.'
        )
        json_blank.update({student_username: student_reply})
        with open('student_blank.json', 'w', encoding='utf-8') as file:
                json.dump(json_blank, file, ensure_ascii=False)
        student_blank.clear


def student_negative_choice(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    student_reply = update.effective_message.text
    if student_reply == 'Не подходит':
        context.bot.send_message(
            chat_id=chat_id,
            text='К сожалению, другого времени на данную неделю нет.Мы запишем вас на следующую неделю.'
        )


def handle_user_reply(update:Update, context:CallbackContext):
    
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

    if user_reply == 'Согласен':
        user_state = 'POSITIVE_CHOICE'
    elif user_reply == 'Не подходит':
        user_state = 'NEGATIVE_CHOICE'
    else:
        user_state = states_database.get(chat_id)

    states_functions = {
        'POSITIVE_CHOICE': student_positive_choice,
        'NEGATIVE_CHOICE': student_negative_choice
    }

    state_handler = states_functions[user_state]
    next_state = state_handler(update, context)
    states_database.update({chat_id: next_state})


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_dotenv()
        telegram_token= os.getenv('TELEGRAM_BOT_TOKEN')
        updater = Updater(telegram_token)
        bot = telegram.Bot(telegram_token)
        last_time_inform(bot)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', handle_user_reply))
        dispatcher.add_handler(MessageHandler(Filters.text, handle_user_reply))
        updater.start_polling()