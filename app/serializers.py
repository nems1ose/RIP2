from rest_framework import serializers

from .models import *


class FilmSerializer(serializers.ModelSerializer):
    # status = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_image(self, film):
        return film.image.url.replace("minio", "localhost", 1)
    
    # def get_status(self, film):
    #     return film.status.name

    class Meta:
        model = Film
        fields = "__all__"

class FilmSerializerUpd(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()

    # def get_image(self, film):
    #     return film.image.url.replace("minio", "localhost", 1)

    class Meta:
        model = Film
        fields = "__all__"


class HistoryStatusesSerializer(serializers.ModelSerializer):

    class Meta:
        model = HistoryStatus
        fields = ("id", "name")


class HistorysSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    moderator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = History
        fields = "__all__"

class HistorySerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    films = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    moderator = serializers.SerializerMethodField()

    def get_owner(self, history):
        return history.owner.username

    def get_moderator(self, history):
        if history.moderator:
            return history.moderator.username
        
    def get_status(self, history):
        return history.status.name
            
    def get_films(self, history):
        items = FilmHistory.objects.filter(history=history)
        return [FilmItemSerializer(item.film, context={"value": item.viewed}).data for item in items]

    class Meta:
        model = History
        fields = '__all__'


class HistorySerializerUpd(HistorysSerializer):
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
