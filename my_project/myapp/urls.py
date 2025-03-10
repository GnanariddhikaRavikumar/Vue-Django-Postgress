from django.urls import path
from .views import CarList, CarDetail, db_check, group_cars,distinct_values, filter_cars

urlpatterns = [
    path('db-check/', db_check, name='db-check'),
    path('cars/', CarList, name='car-list'),  
    path('cars/<int:pk>/', CarDetail, name='car-detail'),
    path('cars/groupcars/<str:column>/', group_cars, name='group_cars'), 
    path("cars/distinct-values/<str:column>/", distinct_values, name="distinct-values"),
    path('cars/filtercar/',filter_cars, name="filter-cars")
]
