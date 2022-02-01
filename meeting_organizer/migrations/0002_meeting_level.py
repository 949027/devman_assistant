# Generated by Django 4.0.1 on 2022-01-26 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting_organizer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='level',
            field=models.CharField(choices=[('novice', 'Новичок'), ('novice+', 'Новичок+'), ('junior', 'Джуниор')], default=1, max_length=200, verbose_name='Уровень'),
            preserve_default=False,
        ),
    ]
