from django.shortcuts import render
from django.http import JsonResponse
from places.models import Place
import json


def home_page(request):
    # Получаем все места из базы данных
    places = Place.objects.all()
    
    # Преобразуем в GeoJSON формат для карты
    places_geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for place in places:
        places_geojson["features"].append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": place.coordinates
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": f"/places/{place.id}/"
            }
        })
    
    # Отладочная информация
    print(f"Found {len(places)} places in database")
    print(f"GeoJSON: {places_geojson}")
    
    # Правильно сериализуем JSON
    places_geojson_json = json.dumps(places_geojson, ensure_ascii=False)
    
    return render(request, 'index.html', {
        'places_geojson': places_geojson_json
    })
