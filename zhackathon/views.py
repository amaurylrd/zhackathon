from collections import OrderedDict
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework import filters
from .filters import CommentFilterSet, RatingFilterSet
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


from rest_framework import viewsets
from rest_framework import generics
from . import models
from . import serializers
from django.core import serializers as django_serializers
from drf_spectacular.utils import extend_schema


class BaseViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        return self.serializers_class.get(self.action, self.serializer_class)


import json


class FestivalViewSet(BaseViewSet, viewsets.ModelViewSet):
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

    queryset = models.Festival.objects.all()
    serializer_class = serializers.FestivalSerializer
    serializers_class = {
        "rating": serializers.EmptySerializer,
        "comments": serializers.EmptySerializer,
    }
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    @extend_schema(responses={200: serializers.AverageRatingSerializer, 204: serializers.EmptySerializer})
    @action(detail=True, methods=["GET"])
    def rating(self, request, *args, **kwargs):
        festival = self.get_object()
        average = festival.get_average_rating()

        if average is None:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = serializers.AverageRatingSerializer(data={"average": average})
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(responses={200: serializers.CommentDetailSerializer})
    @action(detail=True, methods=["GET"])
    def comments(self, request, *args, **kwargs):
        festival = self.get_object()
        comments = festival.get_comments()
        serializer = serializers.CommentDetailSerializer(comments, many=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request, *args, **kwargs):
        return self.__has_permission(super().create, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.__has_permission(super().destroy, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return self.__has_permission(super().update, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def __has_permission(self, func, request, *args, **kwargs):
        if self.request.user.is_staff:
            return func(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentViewSet(BaseViewSet, generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
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

    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentListSerializer
    serializers_class = {
        "create": serializers.CommentDetailSerializer,
        "like": serializers.EmptySerializer,
        "unlike": serializers.EmptySerializer,
        "likes": serializers.EmptySerializer,
    }
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CommentFilterSet
    search_fields = ["festival"]
    ordering_fields = ["created_at", "updated_at"]

    def update(self, request, *args, **kwargs):
        return self.__has_permission(super().update, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.__has_permission(super().partial_update, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.__has_permission(super().destroy, request, *args, **kwargs)

    def __has_permission(self, func, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author == self.request.user:
            return func(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(responses={200: serializers.TotalLikesSerializer})
    @action(detail=True, methods=["POST"])
    def like(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.like(self.request.user)
        serializer = serializers.TotalLikesSerializer(data={"likes": comment.total_likes()})
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(responses={200: serializers.TotalLikesSerializer})
    @action(detail=True, methods=["DELETE"])
    def unlike(self, request, *args, **kwargs):
        comment = self.get_object()
        comment.unlike(self.request.user)
        serializer = serializers.TotalLikesSerializer(data={"likes": comment.total_likes()})
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(responses={200: serializers.TotalLikesSerializer})
    @action(detail=True, methods=["GET"])
    def likes(self, request, *args, **kwargs):
        comment = self.get_object()
        serializer = serializers.TotalLikesSerializer(data={"likes": comment.total_likes()})
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class RatingViewSet(BaseViewSet, generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    # GET /api/ratings/
    # GET /api/ratings/?festival={id}/
    # POST /api/ratings/
    # DELETE /api/ratings/{id}
    # PUT /api/ratings/{id}
    # PATCH /api/ratings/{id}
    queryset = models.Rating.objects.all()
    serializer_class = serializers.RatingListSerializer
    serializers_class = {
        "create": serializers.RatingDetailSerializer,
        "update": serializers.RatingDetailSerializer,
        "partial_update": serializers.RatingDetailSerializer,
    }
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = RatingFilterSet
    search_fields = ["festival"]
    ordering_fields = ["rating"]

    # TODO faire has_rate
    # TODO pourquoi put / patch sont en RatingListSerializer sur le site

    def update(self, request, *args, **kwargs):
        return self.__has_permission(super().update, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.__has_permission(super().partial_update, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.__has_permission(super().destroy, request, *args, **kwargs)

    def __has_permission(self, func, request, *args, **kwargs):
        rating = self.get_object()
        if rating.user == self.request.user:
            return func(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)


# class UserView(ViewSet):
#     @action(detail=False, methods=["post"])
#     def login(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         if not username or not password:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(request, username=username, password=password)
#         if user is None or not user.is_active:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         login(request, user)

#         return Response(status=status.HTTP_200_OK)

#     @action(detail=False, methods=["post"])
#     def logout(self, request):
#         logout(request)
#         return Response(status=status.HTTP_200_OK)


# class LoginView(APIView):
#     permission_classes = (AllowAny,)
#     # model = User

#     def post(self, request, format=None):
#         serializer = LoginSerializer(data=self.request.data, context={"request": self.request})
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data["user"]
#         login(request, user)

#         return Response(status=status.HTTP_202_ACCEPTED)


# from rest_framework import viewsets


# class AdminViewSet(viewsets.ViewSet):
#     def dkjfsdkljfjs(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         if not username or not password:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         if not user.check_password(password):
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#         user.is_staff = True
#         user.save()

#         return Response(status=status.HTTP_200_OK)


# from rest_framework.permissions import IsAuthenticated


# class DeleteAccount(APIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, *args, **kwargs):
#         try:
#             user = self.request.user
#             user.delete()
#         except:
#             return Response(status=status.HTTP_)

#         return Response({"result": "user delete"})
