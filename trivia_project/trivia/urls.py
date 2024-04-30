from django.urls import path
from . import views

urlpatterns = [
    path('trivia/', views.trivia_view, name='trivia_view'),
    path('check_answer/', views.check_answer, name='check_answer'),
]