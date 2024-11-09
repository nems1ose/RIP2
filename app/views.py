from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from django.utils import timezone

from app.models import Film, History, FilmHistory


def index(request):
    film_name = request.GET.get("film_name", "")
    films = Film.objects.filter(status=1)

    if film_name:
        films = films.filter(name__icontains=film_name)

    draft_history = get_draft_history()

    context = {
        "film_name": film_name,
        "films": films
    }

    if draft_history:
        context["films_count"] = len(draft_history.get_films())
        context["draft_history"] = draft_history

    return render(request, "films_page.html", context)


def add_film_to_draft_history(request, film_id):
    film = Film.objects.get(pk=film_id)

    draft_history = get_draft_history()

    if draft_history is None:
        draft_history = History.objects.create()
        draft_history.owner = get_current_user()
        draft_history.date_created = timezone.now()
        draft_history.save()

    if FilmHistory.objects.filter(history=draft_history, film=film).exists():
        return redirect("/")

    item = FilmHistory(
        history=draft_history,
        film=film
    )
    item.save()

    return redirect("/")


def film_details(request, film_id):
    context = {
        "film": Film.objects.get(id=film_id)
    }

    return render(request, "film_page.html", context)


def delete_history(request, history_id):
    if not History.objects.filter(pk=history_id).exists():
        return redirect("/")

    with connection.cursor() as cursor:
        cursor.execute("UPDATE historys SET status=5 WHERE id = %s", [history_id])

    return redirect("/")


def history(request, history_id):
    if not History.objects.filter(pk=history_id).exists():
        return redirect("/")

    history = History.objects.get(id=history_id)
    if history.status == 5:
        return redirect("/")

    context = {
        "history": history,
    }

    return render(request, "history_page.html", context)


def get_draft_history():
    return History.objects.filter(status=1).first()


def get_current_user():
    return User.objects.filter(is_superuser=False).first()