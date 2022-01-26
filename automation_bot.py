from dotenv import load_dotenv
import os
from telegram import Update, chat, replymarkup
from telegram.ext import Filters
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
import json


states_database = {}
student_blank = {}


time_keyboard = [['18:00', '18:30', '19:00', '19:30', 'Ни один не подходит']]
skill_keyboard = [['Новичок', 'Джун']]
new_blank_keyboard = [['Изменить время','Выйти']]

def start(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    telegram_id = update.message.from_user.id
    context.bot.send_message(
        chat_id=chat_id,
        text=' Привет, я бот, созданный для упрощения работы по организации проектов для курсов Devman.'
             ' Выберите удобный для вас интервал созвона из списка',
        reply_markup = ReplyKeyboardMarkup(time_keyboard, resize_keyboard=True, one_time_keyboard=True) 
    )
    student_blank.update({'Имя Фамилия': f'{first_name} {last_name}', 'telegram':telegram_id})
    
    return 'TIME'


def make_new_blank(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    telegram_id = update.message.from_user.id
    context.bot.send_message(
        chat_id=chat_id,
        text=' Выберите удобный для вас интервал созвона из списка',
        reply_markup = ReplyKeyboardMarkup(time_keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
     

def get_student_time(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    student_time = update.effective_message.text
    context.bot.send_message(
        chat_id=chat_id,
        text = f'Вы выбрали созвон, который начинается в {student_time}'
                'Теперь выберите, к какой категории учеников вы относитесь',
        reply_markup = ReplyKeyboardMarkup(skill_keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    student_blank.update({'Время': student_time})

    return 'SKILL'


def get_student_skill(update:Update, context:CallbackContext):
    chat_id = update.effective_message.chat_id
    student_skill = update.effective_message.text
    student_blank.update({'Уровень': student_skill})
    context.bot.send_message(
        chat_id=chat_id,
        text=f'Ваш уровень - {student_skill}'
    )
    with open('student_blank.json', 'w', encoding='utf-8') as file:
        json.dump(student_blank, file, ensure_ascii=False)


def handle_user_reply(update: Update, context: CallbackContext):
    with open('student_blank.json', 'r', encoding='utf-8') as file:
        json_student_blank = json.load(file)
        student_blank.update(json_student_blank)

    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
        user_id = update.message.from_user.id

    elif update.callback_query:
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return

    if user_reply == '/start':
        if str(user_id) in json_student_blank:
            context.bot.send_message(
                chat_id=chat_id,
                text = 'Вы уже выбрали время созвона, если хотите внести изменения, нажмите соотвествующую кнопку'
                reply_markup = ReplyKeyboardMarkup(resize)
            )
            user_state = 'NEW_BLANK'
        else:     
            user_state = 'START'
    else:
        user_state = states_database.get(chat_id)

    states_functions = {
        'START': start,
        'TIME': get_student_time,
        'SKILL': get_student_skill,
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