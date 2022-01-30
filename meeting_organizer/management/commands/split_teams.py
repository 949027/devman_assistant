from django.core.management.base import BaseCommand
from django.db.models import Count
from datetime import timedelta, datetime, date
import telegram

from meeting_organizer.models import Meeting, Student


class Command(BaseCommand):

    def handle(self, *args, **options):
        levels = ['novice', 'novice+', 'junior']
        free_students = []

        for level in levels:
            d = date(1900, 1, 1)
            for i in Student.objects.all():
                student = Student.objects.get(id=i.id)
                worktime_to = datetime.combine(d, student.worktime_to)
                worktime_from = datetime.combine(d, student.worktime_from)
                student.time_interval = worktime_to-worktime_from
                student.save()
            students_queue = list(Student.objects.filter(level=level).order_by('time_interval'))
            for meeting in Meeting.objects.filter(team_members=None):
                candidates = []

                Meeting.objects.get(id=meeting.id)
                meeting.level = level
                meeting.save()

                for student in students_queue:
                    if student.worktime_from <= meeting.time and student.worktime_to > meeting.time:
                        candidates.append(student)
                candidates_amount = len(candidates)

                if candidates_amount >= 3:
                    for candidate in candidates[:3]:
                        meeting.team_members.through.objects.create(meeting_id=meeting.id, student_id=candidate.id)
                        students_queue.remove(candidate)

                if candidates_amount == 2:
                    for candidate in candidates[:2]:
                        meeting.team_members.through.objects.create(meeting_id=meeting.id, student_id=candidate.id)
                        students_queue.remove(candidate)

                if candidates_amount < 2:
                    Meeting.objects.get(id=meeting.id).delete()

            for student in students_queue:
                free_students.append(student)

        incomplete_teams = Meeting.objects.annotate(num_members=Count('team_members')).filter(num_members=2)
        available_time = []
        for team in incomplete_teams:
            available_time.append(str(team.time))

        #рассылка сообщений свободным ученикам
        for student in free_students:
            text = 'Привет! К сожалению, в удобное для тебя время созвонов нет.\n' \
                   'Сможешь выбрать другой промежуток времени? Для этого нажми ' \
                   f'кнопку "Другое время".\n Вот какое время доступно:\n {available_time}'
            bot = telegram.Bot(token='5003258723:AAFUwJ_Jda918H9OU8Q9DWI1RRtAiw168yw')
            bot.sendMessage(chat_id=student.telegram_chat_id, text=text)