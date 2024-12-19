from django.urls import path
from . import views

app_name = 'booking'
urlpatterns = [
    path('payment/', views.payment, name='payment'),
]
