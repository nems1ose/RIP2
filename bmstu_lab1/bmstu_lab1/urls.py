"""
URL configuration for bmstu_lab1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from lab12 import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.base),
#     path('des/<int:id>/', views.base_des, name='card_url'),
#     path('trash/', views.trash),
# ]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello),
    path('', views.GetFilms),
    path('film/<int:id>/', views.GetFilm, name='film_url'),
    path('history/', views.GetHistory, name='history'),
    path('films/', views.GetFilms),
]
