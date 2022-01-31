from django.core.management.base import BaseCommand
from datetime import timedelta, datetime, date

from meeting_organizer.models import Meeting, Student, ProductManager


class Command(BaseCommand):

    def handle(self, *args, **options):
        d = date(1900, 1, 1)
        for product_manager in ProductManager.objects.all():
            meeting_start = datetime.combine(d, product_manager.worktime_from)
            meeting_end = meeting_start + timedelta(minutes=30)

            while meeting_end <= datetime.combine(d, product_manager.worktime_to):
                Meeting.objects.get_or_create(
                    time=meeting_start,
                    product_manager=ProductManager.objects.get(id=product_manager.id),
                )
                meeting_start += timedelta(minutes=30)
                meeting_end = meeting_start + timedelta(minutes=30)