from django.db import models


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
    description_long = models.TextField(
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
    image = models.ImageField(
        upload_to='places/',
        verbose_name='Изображение',
        help_text='Загрузите изображение места',
        blank=True,
        null=True
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
