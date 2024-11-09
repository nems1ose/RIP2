from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('films/<int:film_id>/', film_details, name="film_details"),
    path('films/<int:film_id>/add_to_history/', add_film_to_draft_history, name="add_film_to_draft_history"),
    path('historys/<int:history_id>/delete/', delete_history, name="delete_history"),
    path('historys/<int:history_id>/', history)
]
