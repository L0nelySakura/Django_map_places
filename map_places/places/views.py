from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Place


def places_list(request):
    """Отображение списка всех мест"""
    places = Place.objects.all()
    return render(request, 'places/places_list.html', {'places': places})


def places_json(request):
    """API для получения мест в формате JSON для карты"""
    places = Place.objects.all()
    places_data = []
    
    for place in places:
        places_data.append({
            'title': place.title,
            'description_short': place.description_short,
            'coordinates': place.coordinates,
            'id': place.id,
            'image_url': place.image.url if place.image else None
        })
    
    return JsonResponse(places_data, safe=False)


def place_detail(request, place_id):
    """Детальная информация о месте - возвращает JSON как текст"""
    try:
        place = Place.objects.get(id=place_id)
        
        # Формируем массив изображений, группируя по позициям
        imgs_by_position = {}
        
        # Группируем фотографии по позициям
        for photo in place.photos.all().order_by('position', 'created_at'):
            if photo.position not in imgs_by_position:
                imgs_by_position[photo.position] = []
            imgs_by_position[photo.position].append(photo.image.url)
        
        # Создаем плоский массив для обратной совместимости
        imgs = []
        for position in sorted(imgs_by_position.keys()):
            imgs.extend(imgs_by_position[position])
        
        # Создаем JSON как строку
        import json
        data = {
            'title': place.title,
            'imgs': imgs,
            'imgs_by_position': imgs_by_position,  # Добавляем группировку по позициям
            'description_short': place.description_short,
            'description_long': place.description_long,
            'coordinates': {
                'lng': str(place.longitude),
                'lat': str(place.latitude)
            }
        }
        
        # Возвращаем JSON как обычный текст
        return HttpResponse(json.dumps(data, ensure_ascii=False, indent=2), 
                          content_type='text/plain; charset=utf-8')
    except Place.DoesNotExist:
        return HttpResponse('{"error": "Place not found"}', 
                          status=404, content_type='text/plain; charset=utf-8')
