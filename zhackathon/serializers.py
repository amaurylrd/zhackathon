# pylint: disable=abstract-method

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import models


class EmptySerializer(serializers.Serializer):
    class Meta:
        fields = ()


class FestivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Festival
        fields = "__all__"


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ["festival", "content"]
        read_only_fields = ["author"]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ["content"]


class RatingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rating
        fields = ["festival"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class RatingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rating
        fields = ["festival", "rating"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class AverageRatingSerializer(serializers.Serializer):
    average = serializers.FloatField()

    class Meta:
        fields = ["average"]


class TotalLikesSerializer(serializers.Serializer):
    total = serializers.IntegerField()

    class Meta:
        fields = ["total"]


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, validators=[UniqueValidator(User.objects.all())])
    email = serializers.EmailField(validators=[UniqueValidator(User.objects.all())])
    password = serializers.CharField(write_only=True, validators=[validate_password], style={"input_type": "password"})
    password_confirmation = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirmation")

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password_confirmation"):
            raise serializers.ValidationError({"password": _("Password fields didn't match.")}, code="authorization")

        return attrs


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        fields = ("username", "password")
