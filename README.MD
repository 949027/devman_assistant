База данных:
1. Cоздать виртуальное окружение 
2. pip install -r requirements.txt
3. python manage.py makemigrations (создать миграцию)
4. python manage.py migrate (провести миграции)
5. python manage.py createsuperuser (создать суперпользователя для входа в админку)
6. python manage.py runserver (запустить сервер)
7. http://127.0.0.1:8000/admin/ (админка)
8. python manage.py automation_bot (запустить бота в отдельной консоли)
9. python manage.py create_teams (создать пустые встречи, предварительно нужно заполнить в админке хотя бы одного ПМа)
10. python manage.py split_teams (распределить учеников по командам, предварительно нужно в админке добавить учеников)
Для повторного распределения нужно либо удалить данные в таблице "meeting_organizer_meeting_team_members" (я через DB browser делаю) либо удалить базу (чтобы не заполнять ее каждый раз - можно заранее сделать копию базы).
11. python manage.py inform_bot (Новый бот, который оповещает о последнем времени созвона и ждет ответа от студента: согласиться или откажеться)

## Бот
Создайте файл `.env` в него передайте переменной `TELEGRAM_BOT_TOKEN` телеграм токен(его нужно создать у отца ботов),пример:
```
TELEGRAM_BOT_TOKEN=67wqedg823in0d

```