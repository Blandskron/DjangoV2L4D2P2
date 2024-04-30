from django.urls import path
from . import views

app_name = 'trivia'

urlpatterns = [
    path('', views.trivia_view, name='trivia'),
    path('restart/', views.restart_game, name='restart'),
]