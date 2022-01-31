import logging

from django.core.management.base import BaseCommand
from django.db.models import Count, Q
from datetime import timedelta, datetime, date
import telegram

from meeting_organizer.models import Meeting, Student


class Command(BaseCommand):

    def handle(self, *args, **options):
        for student in Student.objects.filter(meetings=None):
            for meeting in Meeting.objects.annotate(num_members=Count('team_members')).filter(num_members=2):
                if student.worktime_from <= meeting.time and student.worktime_to > meeting.time and meeting.level == student.level:
                    meeting.team_members.through.objects.create(meeting_id=meeting.id, student_id=student.id)

                    text = f'Ты добавлен в команду! Твое время для созвона: {meeting.time}'
                    bot = telegram.Bot(token='5003258723:AAFUwJ_Jda918H9OU8Q9DWI1RRtAiw168yw')
                    try:
                        bot.sendMessage(chat_id=student.telegram_chat_id, text=text)
                    except telegram.error.BadRequest:
                        logging.warning(f'Message for {student} was not sent')









