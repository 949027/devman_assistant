from django.db import models


class ProductManager(models.Model):
    name = models.CharField('Имя продукт-менеджера', max_length=200)
    worktime_from = models.TimeField('Рабочее время, с')
    worktime_to = models.TimeField('Рабочее время, до')
    telegram_username = models.CharField('Юзернейм в телеграме', max_length=200)

    def __str__(self):
        return self.name


class Student(models.Model):
    LEVEL = (
        ('novice', 'Новичок'), ('novice+', 'Новичок+'), ('junior', 'Джуниор')
    )

    name = models.CharField('Имя ученика', max_length=200)
    level = models.CharField('Уровень', max_length=200, choices=LEVEL)
    worktime_from = models.TimeField('Рабочее время, с', blank=True, null=True)
    worktime_to = models.TimeField('Рабочее время, до', blank=True, null=True)
    time_interval = models.CharField('Интервал рабочего времени', null=True, blank=True, max_length=200)
    telegram_username = models.CharField('Юзернейм в телеграме', max_length=200)

    def __str__(self):
        return self.name


class Meeting(models.Model):
    LEVEL = (
        ('novice', 'Новичок'), ('novice+', 'Новичок+'), ('junior', 'Джуниор')
    )

    level = models.CharField('Уровень', max_length=200, choices=LEVEL, blank=True, null=True)
    time = models.TimeField('Время')
    product_manager = models.ForeignKey(
        ProductManager,
        related_name='meetings',
        verbose_name='Продукт-менеджер',
        on_delete=models.CASCADE,
    )
    team_members = models.ManyToManyField(
        Student,
        related_name='meetings',
        verbose_name='Члены команды',
        blank=True,
    )
