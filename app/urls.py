from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/films/', search_films),  # GET
    path('api/films/<int:film_id>/', get_film_by_id),  # GET
    path('api/films/<int:film_id>/update/', update_film),  # PUT
    path('api/films/<int:film_id>/update_image/', update_film_image),  # POST
    path('api/films/<int:film_id>/delete/', delete_film),  # DELETE
    path('api/films/create/', create_film),  # POST
    path('api/films/<int:film_id>/add_to_history/', add_film_to_history),  # POST

    # Набор методов для заявок
    path('api/historys/', search_historys),  # GET
    path('api/historys/<int:history_id>/', get_history_by_id),  # GET
    path('api/historys/<int:history_id>/update/', update_history),  # PUT
    path('api/historys/<int:history_id>/update_status_user/', update_status_user),  # PUT
    path('api/historys/<int:history_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/historys/<int:history_id>/delete/', delete_history),  # DELETE

    # Набор методов для м-м
    path('api/historys/<int:history_id>/update_film/<int:film_id>/', update_film_in_history),  # PUT
    path('api/historys/<int:history_id>/delete_film/<int:film_id>/', delete_film_from_history),  # DELETE

    # Набор методов для аутентификации и авторизации
    path("api/users/register/", register),  # POST
    path("api/users/login/", login),  # POST
    path("api/users/logout/", logout),  # POST
    path("api/users/<int:user_id>/update/", update_user)  # PUT
]
