from django.urls import path
from . import views

urlpatterns = [
    # Quand on arrive sur /countries/ (vide après le slash), on lance la vue country_list
    path('', views.country_list, name='country_list'),
    path('stats/', views.stats_view, name='stats'),
    path('<str:cca3>/', views.country_detail, name='country_detail'),
]