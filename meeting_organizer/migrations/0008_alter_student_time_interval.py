# Generated by Django 4.0.1 on 2022-01-27 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_organizer', '0007_alter_student_time_interval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='time_interval',
            field=models.TimeField(blank=True, null=True, verbose_name='Интервал рабочего времени'),
        ),
    ]
