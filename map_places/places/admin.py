from django.contrib import admin
from django.utils.html import format_html
from .models import Place, Photo


class PhotoInline(admin.TabularInline):
    """Inline админка для фотографий"""
    model = Photo
    extra = 0  # Не добавляем пустые строки автоматически
    fields = ('image', 'position')
    ordering = ('position',)
    help_text = 'Позиция определяет группу фотографий для карусели'


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'latitude', 'longitude', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description_short')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PhotoInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description_short', 'description_long')
        }),
        ('Координаты', {
            'fields': ('latitude', 'longitude')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('place', 'position', 'created_at')
    list_filter = ('place', 'created_at')
    search_fields = ('place__title',)
    ordering = ('place', 'position')
