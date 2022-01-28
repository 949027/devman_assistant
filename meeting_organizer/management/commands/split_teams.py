from django.core.management.base import BaseCommand
from django.db.models import Count
from datetime import timedelta, datetime, date

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
                for student in students_queue:
                    if student.worktime_from <= meeting.time and student.worktime_to > meeting.time:
                        candidates.append(student)
                candidates_amount = len(candidates)

                if candidates_amount >= 3:
                    for candidate in candidates[:3]:
                        meeting.team_members.through.objects.create(meeting_id=meeting.id, student_id=candidate.id)
                        students_queue.remove(candidate)

            for student in students_queue:
                free_students.append(student) # студенты которым не хватило места
