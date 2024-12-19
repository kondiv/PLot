from django.urls import path
from . import views

app_name = 'parking'
urlpatterns = [
    path('add_parking/', views.add_parking, name='add_parking'),
    path('all_parking_map/', views.all_parking_map, name='all-parking-map'),
    path('booking_confirmation/', views.booking_confirmation, name='booking_confirmation'),
]
