База данных:
1. Cоздать виртуальное окружение 
2. pip install -r requirements.txt
3. python manage.py makemigrations (создать миграцию)
4. python manage.py migrate (провести миграции)
5. python manage.py createsuperuser (создать суперпользователя для входа в админку)
6. python manage.py runserver (запустить сервер)
7. http://127.0.0.1:8000/admin/ (админка)
8. ?

## Бот
Создайте файл `.env` в него передайте переменной `TELEGRAM_BOT_TOKEN` телеграм токен(его нужно создать у отца ботов),пример:
```
TELEGRAM_BOT_TOKEN=67wqedg823in0d

```