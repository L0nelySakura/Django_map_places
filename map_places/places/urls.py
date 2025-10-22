from django.urls import path
from . import views

app_name = 'places'

urlpatterns = [
    path('', views.places_list, name='places_list'),
    path('api/', views.places_json, name='places_json'),
    path('<int:place_id>/', views.place_detail, name='place_detail'),
]
