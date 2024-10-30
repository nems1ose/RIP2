import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


def get_draft_history():
    return History.objects.filter(status=1).first()


def get_user():
    return User.objects.filter(is_superuser=False).first()


def get_moderator():
    return User.objects.filter(is_superuser=True).first()


@api_view(["GET"])
def search_films(request):
    film_name = request.GET.get("film_name", "")

    films = Film.objects.filter(status=1)

    if film_name:
        films = films.filter(name__icontains=film_name)

    serializer = FilmSerializer(films, many=True)

    draft_history = get_draft_history()

    resp = {
        "films": serializer.data,
        "films_count": len(serializer.data),
        "draft_history": draft_history.pk if draft_history else None
    }

    return Response(resp)


@api_view(["GET"])
def get_film_by_id(request, film_id):
    if not Film.objects.filter(pk=film_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    film = Film.objects.get(pk=film_id)
    serializer = FilmSerializer(film, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_film(request, film_id):
    if not Film.objects.filter(pk=film_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    film = Film.objects.get(pk=film_id)

    image = request.data.get("image")
    if image is not None:
        film.image = image
        film.save()

    serializer = FilmSerializer(film, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def create_film(request):
    Film.objects.create()

    films = Film.objects.filter(status=1)
    serializer = FilmSerializer(films, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_film(request, film_id):
    if not Film.objects.filter(pk=film_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    film = Film.objects.get(pk=film_id)
    film.status = 2
    film.save()

    films = Film.objects.filter(status=1)
    serializer = FilmSerializer(films, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_film_to_history(request, film_id):
    if not Film.objects.filter(pk=film_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    film = Film.objects.get(pk=film_id)

    draft_history = get_draft_history()

    if draft_history is None:
        draft_history = History.objects.create()
        draft_history.owner = get_user()
        draft_history.date_created = timezone.now()
        draft_history.save()

    if FilmHistory.objects.filter(history=draft_history, film=film).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    item = FilmHistory.objects.create()
    item.history = draft_history
    item.film = film
    item.save()

    serializer = HistorySerializer(draft_history)
    return Response(serializer.data["films"])


@api_view(["POST"])
def update_film_image(request, film_id):
    if not Film.objects.filter(pk=film_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    film = Film.objects.get(pk=film_id)

    image = request.data.get("image")
    if image is not None:
        film.image = image
        film.save()

    serializer = FilmSerializer(film)

    return Response(serializer.data)


@api_view(["GET"])
def search_historys(request):
    status = int(request.GET.get("status", 0))
    date_formation_start = request.GET.get("date_formation_start")
    date_formation_end = request.GET.get("date_formation_end")

    historys = History.objects.exclude(status__in=[1, 5])

    if status > 0:
        historys = historys.filter(status=status)

    if date_formation_start and parse_datetime(date_formation_start):
        historys = historys.filter(date_formation__gte=parse_datetime(date_formation_start))

    if date_formation_end and parse_datetime(date_formation_end):
        historys = historys.filter(date_formation__lt=parse_datetime(date_formation_end))

    serializer = HistorysSerializer(historys, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_history_by_id(request, history_id):
    if not History.objects.filter(pk=history_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    history = History.objects.get(pk=history_id)
    serializer = HistorySerializer(history, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_history(request, history_id):
    if not History.objects.filter(pk=history_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    history = History.objects.get(pk=history_id)
    serializer = HistorySerializer(history, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, history_id):
    if not History.objects.filter(pk=history_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    history = History.objects.get(pk=history_id)

    if history.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    history.status = 2
    history.date_formation = timezone.now()
    history.save()

    serializer = HistorySerializer(history, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, history_id):
    if not History.objects.filter(pk=history_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    history = History.objects.get(pk=history_id)

    if history.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    history.date_complete = timezone.now()
    history.status = request_status
    history.moderator = get_moderator()
    history.save()

    serializer = HistorySerializer(history, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_history(request, history_id):
    if not History.objects.filter(pk=history_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    history = History.objects.get(pk=history_id)

    if history.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    history.status = 5
    history.save()

    serializer = HistorySerializer(history, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_film_from_history(request, history_id, film_id):
    if not FilmHistory.objects.filter(history_id=history_id, film_id=film_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = FilmHistory.objects.get(history_id=history_id, film_id=film_id)
    item.delete()

    history = History.objects.get(pk=history_id)

    serializer = HistorySerializer(history, many=False)
    films = serializer.data["films"]

    if len(films) == 0:
        history.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(films)


@api_view(["PUT"])
def update_film_in_history(request, history_id, film_id):
    if not FilmHistory.objects.filter(film_id=film_id, history_id=history_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = FilmHistory.objects.get(film_id=film_id, history_id=history_id)

    serializer = FilmHistorySerializer(item, data=request.data,  partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def logout(request):
    return Response(status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_user(request, user_id):
    if not User.objects.filter(pk=user_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = User.objects.get(pk=user_id)
    serializer = UserSerializer(user, data=request.data, partial=True)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    serializer.save()

    return Response(serializer.data)