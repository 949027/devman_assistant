# Generated by Django 4.0.1 on 2022-01-28 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_organizer', '0011_alter_student_time_interval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='time_interval',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Интервал рабочего времени'),
        ),
    ]
