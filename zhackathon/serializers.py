from django.contrib.auth.password_validation import validate_password
from django.utils.text import gettext_lazy as _
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


class RatingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rating
        fields = ["festival", "rating"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


# class RegisterSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(write_only=True, validators=[UniqueValidator(User.objects.all())])
#     email = serializers.EmailField(validators=[UniqueValidator(User.objects.all())])
#     password = serializers.CharField(write_only=True, validators=[validate_password], style={"input_type": "password"})
#     password_confirmation = serializers.CharField(write_only=True, style={"input_type": "password"})

#     class Meta:
#         model = User
#         fields = ("username", "email", "password", "password_confirmation")

#     def validate(self, attrs):
#         if attrs.get("password") != attrs.get("password_confirmation"):
#             raise serializers.ValidationError({"password": _("Password fields didn't match.")}, code="authorization")

#         return attrs

#     def create(self, validated_data):
#         user = User.objects.create_user(username=validated_data["username"], email=validated_data["email"])
#         user.set_password(validated_data["password"])
#         user.is_active = True
#         user.save()

#         return user


## here


# class Festival2Serializer(ModelSerializer):
#     class Meta:
#         model = Festival
#         fields = "__all__"


# class LoginSerializer(Serializer):
#     username = CharField(write_only=True)
#     password = CharField(write_only=True, style={"input_type": "password"}, trim_whitespace=False)

#     def validate(self, attrs):
#         username = attrs.get("username")
#         password = attrs.get("password")

#         if not username or not password:
#             raise ValidationError({"password": _("Both 'username' and 'password' are required.")}, code="authorization")

#         # todo decoder password
#         user = authenticate(request=self.context.get("request"), username=username, password=password)
#         if not user:
#             raise ValidationError(_("Access denied: wrong username or password."), code="authorization")
#         attrs["user"] = user

#         return attrs
