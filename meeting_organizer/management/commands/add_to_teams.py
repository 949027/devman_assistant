import logging
from os import getenv

from django.core.management.base import BaseCommand
from django.db.models import Count
from dotenv import load_dotenv
import telegram

from meeting_organizer.models import Meeting, Student


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_dotenv()
        token = getenv('TELEGRAM_BOT_TOKEN')

        incomplete_teams = Meeting.objects.annotate(
            num_members=Count('team_members')
        ).filter(num_members=2)

        for student in Student.objects.filter(meetings=None):
            for teams in incomplete_teams:
                if student.worktime_from <= teams.time < student.worktime_to \
                        and teams.level == student.level:

                    teams.team_members.through.objects.create(
                        meeting_id=teams.id,
                        student_id=student.id,
                    )

                    text = f'Ты добавлен в команду! Твое время для созвона:' \
                           f' {teams.time}'
                    bot = telegram.Bot(token=token)
                    try:
                        bot.sendMessage(
                            chat_id=student.telegram_chat_id,
                            text=text,
                        )
                    except telegram.error.BadRequest:
                        logging.warning(f'Message for {student} was not sent')
