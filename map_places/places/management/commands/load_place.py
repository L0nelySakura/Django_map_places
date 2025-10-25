import json
import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from ...models import Place, Photo
from urllib.parse import urlparse
import os


class Command(BaseCommand):
    help = 'Load place from JSON file or URL'

    def add_arguments(self, parser):
        parser.add_argument('source', type=str, help='JSON file path or URL')

    def handle(self, *args, **options):
        source = options['source']

        self.stdout.write(f'Loading from: {source}')

        try:
            # Загружаем JSON - ИСПРАВЛЕННЫЙ ВЫЗОВ МЕТОДА
            place_data = self.load_json(source)

            # Обрабатываем данные
            self.process_place_data(place_data)

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )

    def load_json(self, source):  # ← ДОБАВЛЕН МЕТОД load_json
        """Загружает JSON из файла или URL"""
        if source.startswith(('http://', 'https://')):
            response = requests.get(source)
            response.raise_for_status()
            return response.json()
        else:
            # Локальный файл
            with open(source, 'r', encoding='utf-8') as f:
                return json.load(f)

    def process_place_data(self, data):
        """Обрабатывает данные места"""

        # Если data - список, обрабатываем каждый элемент
        if isinstance(data, list):
            for item in data:
                self.create_or_update_place(item)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully loaded {len(data)} places')
            )
        else:
            # Если data - одиночный объект
            self.create_or_update_place(data)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully loaded place: {data.get("title", "Unknown")}')
            )

    def create_or_update_place(self, data):
        """Создает или обновляет место"""

        # Валидация обязательных полей
        required_fields = ['title', 'coordinates']
        for field in required_fields:
            if field not in data:
                raise ValueError(f'Missing required field: {field}')

        # Проверяем существование места
        try:
            place = Place.objects.get(title=data['title'])
            self.stdout.write(f'Updating existing place: {data["title"]}')
        except Place.DoesNotExist:
            place = Place(title=data['title'])
            self.stdout.write(f'Creating new place: {data["title"]}')

        # Обновляем данные
        place.description_short = data.get('description_short', '')
        place.description_long = data.get('description_long', '')
        place.latitude = data['coordinates']['lat']
        place.longitude = data['coordinates']['lng']
        place.save()

        # Добавляем фотографии
        self.add_photos(place, data.get('imgs', []))

    def add_photos(self, place, image_urls):
        """Добавляет фотографии к месту"""
        for position, img_url in enumerate(image_urls, 1):
            try:
                self.stdout.write(f'Loading image {position}: {img_url}')

                response = requests.get(img_url, timeout=30)
                response.raise_for_status()

                # Создаем имя файла
                filename = os.path.basename(urlparse(img_url).path)
                if not filename:
                    filename = f'photo_{place.id}_{position}.jpg'

                # Создаем объект Photo
                photo = Photo(place=place, position=position)
                photo.image.save(filename, ContentFile(response.content))

                self.stdout.write(f'✓ Added photo: {filename}')

            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'✗ Failed to load image: {str(e)}')
                )