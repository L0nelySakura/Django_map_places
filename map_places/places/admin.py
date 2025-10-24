from django.contrib import admin
from django.utils.html import format_html
from django.forms import ModelForm
from django import forms
from .models import Place, Photo


class PhotoForm(ModelForm):
    """Форма с превью для фотографий"""
    
    class Meta:
        model = Photo
        fields = '__all__'
        widgets = {
            'image': forms.FileInput(attrs={'onchange': 'previewImage(this)'})
        }


class PhotoInline(admin.TabularInline):
    """Inline админка для фотографий с превью"""
    model = Photo
    form = PhotoForm
    extra = 0  # Не добавляем пустые строки автоматически
    fields = ('image', 'preview', 'position')
    can_delete = True
    readonly_fields = ('preview',)
    ordering = ('position',)
    help_text = 'Позиция определяет группу фотографий для карусели'
    
    def preview(self, obj):
        """Превью фотографии"""
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 80px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">Нет изображения</span>')
    preview.short_description = 'Превью'


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
    
    class Media:
        js = ('admin/js/photo_preview.js',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('place', 'position', 'created_at')
    list_filter = ('place', 'created_at')
    search_fields = ('place__title',)
    ordering = ('place', 'position')
