from django.db import models
from django.core.exceptions import ValidationError
import os
from tinymce.models import HTMLField


def validate_image_file(value):
    """Валидация формата изображения"""
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(f'Недопустимый формат файла. Разрешены только: {", ".join(allowed_extensions)}')


class Place(models.Model):
    """Модель для хранения информации о местах на карте"""
    title = models.CharField(
        max_length=200,
        verbose_name='Название места',
        help_text='Введите название места'
    )
    description_short = models.TextField(
        verbose_name='Краткое описание',
        help_text='Краткое описание места'
    )
    description_long = HTMLField(  # Изменяем здесь
        verbose_name='Подробное описание',
        help_text='Подробное описание места'
    )
    latitude = models.FloatField(
        verbose_name='Широта',
        help_text='Широта в десятичных градусах'
    )
    longitude = models.FloatField(
        verbose_name='Долгота',
        help_text='Долгота в десятичных градусах'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        ordering = ['title']

    def __str__(self):
        return self.title

    @property
    def coordinates(self):
        """Возвращает координаты в формате [долгота, широта] для GeoJSON/Leaflet"""
        return [self.longitude, self.latitude]


class Photo(models.Model):
    """Модель для фотографий мест"""
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name='Место'
    )
    image = models.ImageField(
        upload_to='places/photos/',
        verbose_name='Фотография',
        validators=[validate_image_file]
    )
    position = models.PositiveIntegerField(
        verbose_name='Позиция',
        help_text='Группа фотографий для карусели (1, 2, 3...)',
        default=0
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ['position', 'created_at']

    def __str__(self):
        return f'{self.place.title} - Фото {self.position}'

    def save(self, *args, **kwargs):
        if not self.position or self.position == 0:
            max_position = Photo.objects.filter(
                place=self.place
            ).aggregate(models.Max('position'))['position__max']
            self.position = (max_position or 0) + 1
        super().save(*args, **kwargs)
