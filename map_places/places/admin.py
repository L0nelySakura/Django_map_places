from django.contrib import admin
from django.utils.html import format_html
from django.forms import ModelForm
from django import forms
from .models import Place, Photo


class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = '__all__'
        widgets = {
            'position': forms.HiddenInput(),
            'image': forms.FileInput(attrs={'onchange': 'previewImage(this)'})
        }


class PhotoInline(admin.TabularInline):
    model = Photo
    form = PhotoForm
    extra = 0
    fields = ('drag_handle', 'image', 'preview', 'position')
    readonly_fields = ('preview', 'drag_handle')
    ordering = ('position',)
    can_delete = True

    def drag_handle(self, obj):
        """Иконка для перетаскивания"""
        return format_html('<span class="drag-handle">⋮-⋮</span>')

    drag_handle.short_description = 'Смена позиции'

    def preview(self, obj):
        """Превью фотографии"""
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 80px; object-fit: contain; border: 1px solid #ddd; border-radius: 4px;" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">Нет изображения</span>')

    preview.short_description = 'Превью'

    class Media:
        css = {
            'all': ('admin/css/photo_sortable.css',)
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.14.0/Sortable.min.js',
            'admin/js/photo_sortable.js',
            'admin/js/photo_preview.js',  # ваш существующий файл
        )


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
        css = {
            'all': ('admin/css/photo_sortable.css',)
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.14.0/Sortable.min.js',
            'admin/js/photo_sortable.js',
        )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('place', 'position', 'created_at')
    list_filter = ('place', 'created_at')
    search_fields = ('place__title',)
    ordering = ('place', 'position')

    class Media:
        css = {
            'all': ('admin/css/photo_sortable.css',)
        }