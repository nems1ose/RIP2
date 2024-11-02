from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Film(models.Model):
    STATUS_CHOICES = (
        ("activ", 'Действует'),
        ("delet", 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название", blank=True)
    status = models.CharField(choices=STATUS_CHOICES, default="activ", verbose_name="Статус")
    image = models.ImageField(default="default.png", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)

    time = models.IntegerField(blank=True)
    year = models.IntegerField(blank=True)
    country = models.CharField(blank=True)

    def get_image(self):
        return self.image.url.replace("minio", "localhost", 1)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        db_table = "films"


class History(models.Model):
    STATUS_CHOICES = (
        ("putin", 'Введён'),
        ("atwor", 'В работе'),
        ("compl", 'Завершен'),
        ("rejec", 'Отклонен'),
        ("delet", 'Удален')
    )

    status = models.CharField(choices=STATUS_CHOICES, default="putin", verbose_name="Статус")
    date_created = models.DateTimeField(default=timezone.now(), verbose_name="Дата создания")
    date_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Пользователь", null=True, related_name='owner')
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Модератор", null=True, related_name='moderator')

    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return "История №" + str(self.pk)

    class Meta:
        verbose_name = "История"
        verbose_name_plural = "Истории"
        ordering = ('-date_formation',)
        db_table = "historys"


class FilmHistory(models.Model):
    film = models.ForeignKey(Film, models.DO_NOTHING, blank=True, null=True)
    history = models.ForeignKey(History, models.DO_NOTHING, blank=True, null=True)
    value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "м-м №" + str(self.pk)

    class Meta:
        verbose_name = "м-м"
        verbose_name_plural = "м-м"
        db_table = "film_history"
        unique_together = ('film', 'history')
