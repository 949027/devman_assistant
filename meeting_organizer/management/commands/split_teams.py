from datetime import timedelta, datetime, date
import logging
from os import getenv

from django.core.management.base import BaseCommand
from django.db.models import Count, Q
from dotenv import load_dotenv
import telegram

from meeting_organizer.models import Meeting, Student


def send_message(student, text, token):
    bot = telegram.Bot(token=token)
    try:
        bot.sendMessage(chat_id=student.telegram_chat_id, text=text)
        logging.warning(f'Message for {student} was sent')
    except telegram.error.BadRequest:
        pass

def delete_empty_meetings():
    for meeting in Meeting.objects.filter(team_members=None):
        Meeting.objects.get(id=meeting.id).delete()

def assemble_team(meeting, members, students_queue, token, members_amount):
    for member in members[:members_amount]:

        meeting.team_members.through.objects.create(meeting_id=meeting.id, student_id=member.id)
        students_queue.remove(member)
        text = f'Команда скомплектована! Твое время для созвона: {meeting.time}'
        send_message(member, text, token)

def calculate_time_intervale(found_student):
    d = date(1900, 1, 1)
    student = Student.objects.get(id=found_student.id)
    worktime_to = datetime.combine(d, student.worktime_to)
    worktime_from = datetime.combine(d, student.worktime_from)
    student.time_interval = worktime_to - worktime_from
    student.save()

def set_meeting_level(meeting, level):
    Meeting.objects.get(id=meeting.id)
    meeting.level = level
    meeting.save()

def check_available_time():
    available_time = []
    incomplete_teams = Meeting.objects.annotate(num_members=Count('team_members')).filter(num_members=2)

    for team in incomplete_teams:
        available_time.append(str(team.time))

    return available_time


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_dotenv()
        token = getenv('TELEGRAM_BOT_TOKEN')
        levels = ['novice', 'novice+', 'junior']

        free_students = []

        for level in levels:
            for student in Student.objects.filter(meetings=None):
                calculate_time_intervale(student)

            students_queue = list(Student.objects.filter(level=level).order_by('time_interval'))

            for meeting in Meeting.objects.filter(team_members=None):
                set_meeting_level(meeting, level)

                candidates = []
                for student in students_queue:
                    if student.worktime_from <= meeting.time and student.worktime_to > meeting.time:
                        candidates.append(student)

                candidates_amount = len(candidates)

                if candidates_amount >= 3:
                    assemble_team(meeting, candidates, students_queue, token, members_amount=3)

                if candidates_amount == 2:
                    assemble_team(meeting, candidates, students_queue, token, members_amount=2)

            for student in students_queue:
                free_students.append(student)

            available_time = check_available_time()

            for student in free_students:
                text = 'Привет! К сожалению, в удобное для тебя время созвонов нет.\n' \
                       'Сможешь выбрать другой промежуток времени? Для этого нажми ' \
                       f'кнопку "Другое время".\n Вот какое время доступно:\n {available_time}'
                send_message(student, text, token)

        delete_empty_meetings()