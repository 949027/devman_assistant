from pydoc import text
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

from meeting_organizer.models import Meeting, Student, ProductManager


states_database = {}
student_blank = {}
json_blank = {}        # Записать в базу


time_keyboard = [['18:00-18:30', '18:30-19:00', '19:00-19:30', '19:30-20:00', 'Любое время', 'Ни один не подходит']]
new_blank_keyboard = [['Изменить время','Выйти']]
time_choice_keyboard = [['Принять', 'Конкретное время', 'Другое время']]


def start(update:Update, context:CallbackContext):
    min_time = ProductManager.objects.order_by('worktime_from').first().worktime_from
    max_time = ProductManager.objects.order_by('-worktime_to').first().worktime_to
    chat_id = update.effective_message.chat_id
    context.bot.send_message(
        chat_id=chat_id,
        text=' Привет, я бот, созданный для упрощения работы по организации проектов для курсов Devman.\n'
             ' Интервал созвонов полчаса, поэтому выбирайте начало либо в :00 минут, либо в :30.\n'   
             f' Удобно ли вам созваниваться в один из промежутков с {min_time} до {max_time}? Если подойдет любое время из этого промежутка, нажмите Принять.\n'
             ' Если вам будет удобно конкретное время из этого промежутка, нажмите Конкретное время.\n'
             ' Если же вам не подходит данное время, нажмите Другое время.',
             reply_markup=ReplyKeyboardMarkup(time_choice_keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    
    return 'CHOICE'


def make_new_blank(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    student_username = update.effective_message.from_user.username
    student_id = update.effective_message.from_user.username
    #last_student_time = json_blank[student_id]
    db_student = Student.objects.get(telegram_username=student_username)
    context.bot.send_message(
        chat_id=chat_id,
        text=f'Вы уже указывали время созвона {db_student.worktime_from} - {db_student.worktime_to}.\n'
             'Если вы хотите изменить его, выберите соответствующий пункт меню.',
        reply_markup = ReplyKeyboardMarkup(new_blank_keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    print(update.effective_message.chat_id)
    return 'CHOICE_CHECK'


def new_blank_choice_check(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    user_reply = update.effective_message.text
    if user_reply == 'Изменить время':
        context.bot.send_message(
            chat_id=chat_id,
            text= ' Интервал созвонов полчаса, поэтому выбирайте начало либо в :00 минут, либо в :30.\n'   
                ' Удобно ли вам созваниваться в один из промежутков с 18:00 до 20:00? Если подойдет любое время из этого промежутка, нажмите Принять.\n'
                ' Если вам будет удобно конкретное время из этого промежутка, нажмите Конкретное время.\n'
                ' Если же вам не подходит данное время, нажмите Другое время.',
            reply_markup = ReplyKeyboardMarkup(time_choice_keyboard, resize_keyboard=True, one_time_keyboard=True) 
        )
        return 'CHOICE'
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


def get_student_choice(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    student_username = update.effective_message.from_user.username
    student_reply = update.effective_message.text
    if student_reply == 'Принять':
        context.bot.send_message(
            chat_id=chat_id,
            text='Вы выбрали время созвона в промежутке с 18:00 до 20:00. Когда группы будут распределены, конкретное время вам сообщит куратор'
        )
        db_student = Student.objects.get(telegram_username=student_username)
        db_student.worktime_from = '18:00'
        db_student.worktime_to = '20:00'
        db_student.save()
        # student_blank.update({'Время': '18:00-20:00'})
        # json_blank.update({student_username: '18:00-20:00'})
        # with open('student_blank.json', 'w', encoding='utf-8') as file:
        #     json.dump(json_blank, file, ensure_ascii=False)
        # student_blank.clear()
    elif student_reply == 'Конкретное время':
        context.bot.send_message(
            chat_id=chat_id,
            text='Введите начальное время в формате чч:мм (например - 18:00)'
        )
        return 'TIME_FROM'
    elif student_reply == 'Другое время':
        context.bot.send_message(
            chat_id=chat_id,
            text='Напишите нам интервал времени, в которой вам удобно созвониться в формате чч:мм-чч:мм (Например - 10:00-11:00 без пробелов)'
        )
        return 'TIME'
    else:    
        context.bot.send_message(
            chat_id=chat_id,
            text = 'Не понимаю, что вы хотели написать, начните процедуру заново.'
        )
        return 'START'


def get_student_time_from(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    student_username = update.effective_message.from_user.username
    student_reply = update.effective_message.text
    context.bot.send_message(
        chat_id=chat_id,
        text=f'Введите конечное время в формате чч:мм (например - 22:00)'
    )
    context.user_data['time_from'] = student_reply
    return 'TIME_TO'
    # student_blank.update({'Время': student_reply})
    # json_blank.update({student_username: student_reply})
    # with open('student_blank.json', 'w', encoding='utf-8') as file:
    #         json.dump(json_blank, file, ensure_ascii=False)
    # student_blank.clear


def get_student_time_to(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    student_username = update.effective_message.from_user.username

    time_to = update.effective_message.text
    time_from = context.user_data['time_from']
    context.bot.send_message(
        chat_id=chat_id,
        text=f'Вы указали время созвона {time_from} - {time_to} '
    )
    db_student = Student.objects.get(telegram_username=student_username)
    db_student.worktime_from = time_from
    db_student.worktime_to = time_to
    db_student.save()
    # student_blank.update({'Время': student_reply})
    # json_blank.update({student_username: student_reply})
    # with open('student_blank.json', 'w', encoding='utf-8') as file:
    #         json.dump(json_blank, file, ensure_ascii=False)
    # student_blank.clear


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
        if Student.objects.get(telegram_username=username).worktime_from:
            user_state = 'NEW_BLANK'
        else:     
            user_state = 'START'
    else:
        user_state = states_database.get(chat_id)

    states_functions = {
        'START': start,
        'CHOICE': get_student_choice,
        'NEW_BLANK': make_new_blank,
        'CHOICE_CHECK': new_blank_choice_check,
        'TIME_FROM': get_student_time_from,
        'TIME_TO': get_student_time_to,

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
        updater.start_polling()
