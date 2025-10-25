# Django_map_places
Сайт с интерактивной картой, позволяет просматривать известные точки на карте с подробным описанием
## Технологии
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)

## Использование
### Требования
Установите зависимости, указанные [выше](#Технологии)
### Установка и запуск сервиса

1) Скачайте репозиторий: 
```sh
git clone https://github.com/L0nelySakura/Django_map_places
```

2) Перейдите в папку проекта:
```sh
cd Django_map_places/map_places
```

3) Установите библиотеки при помощи
```
pip install -r requirements.txt
```

3) Настройте .env файл исходя из примера (.env.example)

4) Настройка админки:
```sh
python manage.py createsuperuser
```

5) Запуск проекта:
```sh
python manage.py runserver
```

После запуска перейдите в браузере на указанную страницу для тестирования.
Для добавления новых точек перейдите на /admin и пройдите регистрацию.
Можно добавлять новые точки из JSON-файла при помощи
```sh
python manage.py load_place places.json
```
где places.json - ваш файл с информацией

В данный момент сайт работает [по данной ссылке](https://lonelysakura1.pythonanywhere.com/). 
Доступ к админке:
- Login: admin
- Password: 12341234

Загрузка через load_place имеет свои ограничения на pythonanywhere, он не берет данные с http сайтов, а закачка с https возможно только при платном тарифе :)
