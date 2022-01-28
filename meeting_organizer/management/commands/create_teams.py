from django.core.management.base import BaseCommand
from datetime import timedelta, datetime, date

from meeting_organizer.models import Meeting, Student, ProductManager


class Command(BaseCommand):

    def handle(self, *args, **options):
        d = date(1900, 1, 1)
        product_manager = ProductManager.objects.all().first()
        meeting_start = datetime.combine(d, product_manager.worktime_from)
        meeting_end = meeting_start + timedelta(minutes=30)

        while meeting_end < datetime.combine(d, product_manager.worktime_to):
            print(meeting_end)
            meeting_start += timedelta(minutes=30)
            meeting_end = meeting_start + timedelta(minutes=30)
            Meeting.objects.create(
                time=meeting_start,
                product_manager=ProductManager.objects.all().first(),
            )