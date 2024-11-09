from rest_framework import serializers

from .models import *


class FilmsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, film):
        if film.image:
            return film.image.url.replace("minio", "localhost", 1)

        return "http://localhost:9000/images/default.png"

    class Meta:
        model = Film
        fields = ("id", "name", "status", "time", "image")


class FilmSerializer(FilmsSerializer):
    class Meta(FilmsSerializer.Meta):
        model = Film
        fields = FilmsSerializer.Meta.fields + ("description", )


class HistorysSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    moderator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = History
        fields = "__all__"


class HistorySerializer(HistorysSerializer):
    films = serializers.SerializerMethodField()

    def get_films(self, history):
        items = FilmHistory.objects.filter(history=history)
        return [FilmItemSerializer(item.film, context={"viewed": item.viewed}).data for item in items]


class FilmItemSerializer(FilmSerializer):
    viewed = serializers.SerializerMethodField()

    def get_viewed(self, film):
        return self.context.get("viewed")

    class Meta(FilmSerializer.Meta):
        fields = "__all__"


class FilmHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmHistory
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
