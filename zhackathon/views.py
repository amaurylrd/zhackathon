# pylint: disable=too-many-ancestors

from typing import Optional

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from . import serializers
from .filters import CommentFilterSet, RatingFilterSet
from .models import Comment, Festival, Rating


class BaseViewSet(GenericViewSet):
    serializers_class = {}

    def get_serializer_class(self):
        return self.serializers_class.get(self.action, self.serializer_class)


class FestivalViewSet(BaseViewSet, ModelViewSet):
    """
    GET api/festivals/
    GET api/festivals/{id}/
    GET api/festivals/{id}/rating/
    GET api/festivals/{id}/comments/
    POST api/festivals/
    PUT api/festivals/{id}/
    PATCH api/festivals/{id}/
    DELETE api/festivals/{id}/
    """

    queryset = Festival.objects.all()

    serializer_class = serializers.FestivalSerializer
    serializers_class = {
        "rating": serializers.EmptySerializer,
        "comments": serializers.EmptySerializer,
    }

    permission_classes = (IsAuthenticated, IsAdminUser)

    @extend_schema(responses={200: serializers.AverageRatingSerializer, 204: serializers.EmptySerializer})
    @action(detail=True, methods=["GET"])
    def rating(self, request, *args, **kwargs):
        festival: Festival = self.get_object()
        average: Optional[int] = festival.get_average_rating()

        if average is None:
            return Response(status=HTTP_204_NO_CONTENT)

        serializer = serializers.AverageRatingSerializer(data={"average": average})
        serializer.is_valid(raise_exception=True)

        return Response(status=HTTP_200_OK, data=serializer.data)

    @extend_schema(responses={200: serializers.CommentDetailSerializer})
    @action(detail=True, methods=["GET"])
    def comments(self, request, *args, **kwargs):
        festival: Festival = self.get_object()
        comments: QuerySet[Comment] = festival.get_comments()
        serializer = serializers.CommentDetailSerializer(comments, many=True)

        return Response(status=HTTP_200_OK, data=serializer.data)

    def create(self, request, *args, **kwargs):
        return self.__has_permission(super().create, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return self.__has_permission(super().update, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.__has_permission(super().partial_update, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.__has_permission(super().destroy, request, *args, **kwargs)

    def __has_permission(self, func, request, *args, **kwargs):
        if self.request.user.is_staff:
            return func(request, *args, **kwargs)
        return Response(status=HTTP_403_FORBIDDEN)


class CommentViewSet(BaseViewSet, ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    """
    GET /api/comments/?festival={id}/
    GET /api/comments/
    GET /api/comments/{id}/likes/
    POST /api/comments/
    POST /api/comments/{id}/like/
    PUT /api/comments/{id}/
    PATCH /api/comments/{id}/
    DELETE /api/comments/{id}/
    DELETE /api/comments/{id}/unlike/
    """

    queryset = Comment.objects.all()

    serializer_class = serializers.CommentListSerializer
    serializers_class = {
        "create": serializers.CommentDetailSerializer,
        "like": serializers.EmptySerializer,
        "unlike": serializers.EmptySerializer,
        "likes": serializers.EmptySerializer,
    }

    permission_classes = (IsAuthenticated, IsAdminUser)

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = CommentFilterSet
    search_fields = ["festival"]
    ordering_fields = ["created_at", "updated_at"]

    @extend_schema(responses={201: serializers.TotalLikesSerializer})
    @action(detail=True, methods=["POST"])
    def like(self, request, *args, **kwargs):
        comment: Comment = self.get_object()
        comment.like(self.request.user)

        serializer = serializers.TotalLikesSerializer(data={"likes": comment.total_likes()})
        serializer.is_valid(raise_exception=True)

        return Response(status=HTTP_201_CREATED, data=serializer.data)

    @extend_schema(responses={204: serializers.TotalLikesSerializer})
    @action(detail=True, methods=["DELETE"])
    def unlike(self, request, *args, **kwargs):
        comment: Comment = self.get_object()
        comment.unlike(self.request.user)

        serializer = serializers.TotalLikesSerializer(data={"likes": comment.total_likes()})
        serializer.is_valid(raise_exception=True)

        return Response(status=HTTP_204_NO_CONTENT, data=serializer.data)

    @extend_schema(responses={200: serializers.TotalLikesSerializer})
    @action(detail=True, methods=["GET"])
    def likes(self, request, *args, **kwargs):
        comment: Comment = self.get_object()

        serializer = serializers.TotalLikesSerializer(data={"likes": comment.total_likes()})
        serializer.is_valid(raise_exception=True)

        return Response(status=HTTP_200_OK, data=serializer.data)

    def update(self, request, *args, **kwargs):
        return self.__has_permission(super().update, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.__has_permission(super().partial_update, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.__has_permission(super().destroy, request, *args, **kwargs)

    def __has_permission(self, func, request, *args, **kwargs):
        comment: Comment = self.get_object()
        if comment.author == self.request.user:
            return func(request, *args, **kwargs)
        return Response(status=HTTP_403_FORBIDDEN)


class RatingViewSet(BaseViewSet, ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    """
    GET api/ratings/
    GET /api/ratings/?festival={id}/
    POST api/ratings/
    PUT api/ratings/{id}/
    PATCH api/ratings/{id}/
    DELETE api/ratings/{id}/
    """

    queryset = Rating.objects.all()

    serializer_class = serializers.RatingListSerializer
    serializers_class = {
        "create": serializers.RatingDetailSerializer,
        "update": serializers.RatingDetailSerializer,
        "partial_update": serializers.RatingDetailSerializer,
        "has_rated": serializers.RatingListSerializer,
    }

    permission_classes = (IsAuthenticated, IsAdminUser)

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = RatingFilterSet
    search_fields = ["festival"]
    ordering_fields = ["rating"]

    def update(self, request, *args, **kwargs):
        return self.__has_permission(super().update, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.__has_permission(super().partial_update, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.__has_permission(super().destroy, request, *args, **kwargs)

    def __has_permission(self, func, request, *args, **kwargs):
        rating: Rating = self.get_object()
        if rating.user == self.request.user:
            return func(request, *args, **kwargs)
        return Response(status=HTTP_403_FORBIDDEN)


class UserViewSet(BaseViewSet, CreateAPIView):
    """
    POST /api/user/
    PUT /api/user/login/
    PATCH /api/user/login/
    DELETE /api/user/logout/
    """

    queryset = User.objects.all()

    serializer_class = serializers.UserRegisterSerializer
    serializers_class = {
        "login": serializers.UserLoginSerializer,
        "logout": serializers.EmptySerializer,
    }

    permissions_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Response(status=HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user: User = User.objects.create_user(username=request.data["username"], email=request.data["email"])
        user.set_password(request.data["password"])
        user.is_active = True
        user.save()

        return Response(status=HTTP_201_CREATED, data=serializer.data)

    @extend_schema(responses={202: serializers.EmptySerializer})
    @action(detail=False, methods=["PUT", "PATCH"])
    def login(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Response(status=HTTP_403_FORBIDDEN)

        user: User = authenticate(request, username=request.data["username"], password=request.data["password"])

        if user is None or not user.is_active:
            return Response(status=HTTP_400_BAD_REQUEST)

        login(request, user)

        return Response(status=HTTP_202_ACCEPTED)

    @extend_schema(responses={204: serializers.EmptySerializer})
    @action(detail=False, methods=["DELETE"])
    def logout(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response(status=HTTP_403_FORBIDDEN)

        logout(request)

        return Response(status=HTTP_204_NO_CONTENT)
