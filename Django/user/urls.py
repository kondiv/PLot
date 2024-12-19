from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

app_name = 'users'
urlpatterns = [
    path('registration/', views.register, name='registration'),
    path("logout/", views.user_logout, name="logout"),
    path('login/', views.user_login, name='login'),
    path('password_reset/', views.forgot_password, name='password_reset'),
    path('owner_profile/', views.owner_profile, name='owner_profile'),
    path('parkings_and_docs/', views.parkings_and_docs, name='parkings_and_docs'),
    path('finance/', views.finance, name='finance'),
    path('graphics/', views.graphics, name='graphics'),
    path('driver_profile/', views.driver_profile, name='driver_profile'),
    path('feed_back/', views.feed_back, name='feed_back'),
    path('parking_history/', views.parking_history, name='parking_history'),
    path('notices/', views.notices, name='notices'),
    path('promo_codes/', views.promo_codes, name='promo_codes'),
    path('support_and_assistance/', views.support_and_assistance, name='support_and_assistance'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)