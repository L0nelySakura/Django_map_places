from django.shortcuts import render
from django.http import JsonResponse
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
    """Детальная информация о месте"""
    try:
        place = Place.objects.get(id=place_id)
        
        # Если запрос с Accept: application/json, возвращаем JSON
        if request.headers.get('Accept') == 'application/json' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({
                'title': place.title,
                'description_short': place.description_short,
                'description_long': place.description_long,
                'coordinates': place.coordinates,
                'id': place.id,
                'image_url': place.image.url if place.image else None
            })
        
        # Иначе возвращаем HTML страницу
        return render(request, 'places/place_detail.html', {'place': place})
    except Place.DoesNotExist:
        if request.headers.get('Accept') == 'application/json' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({'error': 'Place not found'}, status=404)
        return render(request, 'places/place_not_found.html')
