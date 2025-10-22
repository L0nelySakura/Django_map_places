from django.contrib import admin
from django.utils.html import format_html
from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'latitude', 'longitude', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description_short')
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description_short', 'description_long')
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview')
        }),
        ('Координаты', {
            'fields': ('latitude', 'longitude')
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px; border: 1px solid #ddd; border-radius: 4px;" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = 'Превью изображения'
