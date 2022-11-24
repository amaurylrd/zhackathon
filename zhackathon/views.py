from collections import OrderedDict
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


from rest_framework import viewsets
from rest_framework import generics
from . import models
from . import serializers


class BaseViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        return self.serializers_class.get(self.action, self.serializer_class)


class FestivalViewSet(viewsets.ModelViewSet):
    queryset = models.Festival.objects.all()
    serializer_class = serializers.FestivalSerializer


from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework import filters
from .filters import CommentFilterSet
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import GenericViewSet

from django.contrib.auth.models import User

import logging

logger = logging.getLogger(__name__)


class CommentViewSet(BaseViewSet, ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentListSerializer
    serializers_class = {"create": serializers.CommentDetailSerializer}
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CommentFilterSet
    search_fields = ["festival"]
    ordering_fields = ["created_at", "updated_at"]

    def create(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        print(request.data, args, kwargs)
        return self.__if_author(super().update, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return self.__if_author(super().partial_update, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.__if_author(super().destroy, request, *args, **kwargs)

    def __if_author(self, func, request, *args, **kwargs):
        comment = self.queryset.get(id=kwargs["pk"])
        if comment.author == self.request.user:
            return func(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["POST"])
    def like(self, request, *args, **kwargs):
        comment = self.queryset.get(id=kwargs["pk"])
        comment.like(self.request.user)
        return Response(comment.get_total_likes())

    @action(detail=True, methods=["DELETE"])
    def unlike(self, request, *args, **kwargs):
        comment = self.queryset.get(id=kwargs["pk"])
        comment.unlike(self.request.user)
        return Response(comment.get_total_likes())

    @action(detail=True, methods=["GET"])
    def likes(self, request, *args, **kwargs):
        comment = self.queryset.get(id=kwargs["pk"])
        return Response(comment.get_total_likes())


class RatingViewSet:
    pass


# class FestivalViewSet(BaseViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
#     queryset = Festival.objects.all()
#     serializer_class = ...
#     serializers_class = {
#         "list": ...,
#         "create": ...,
#         "retrieve": ...,
#         "update": ...,
#         "partial_update": ...,
#         "destroy": ...,
#     }

#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)


# class RegisterView(CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = RegisterSerializer


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


# modification de mot de passe
# set admin


# from rest_framework import generics, status, viewsets
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.viewsets import ModelViewSet

# from .models import Festival
# from .serializers import RegisterSerializer


# class FestivalList(generics.ListAPIView):
#     queryset = Festival.objects.all()
#     serializer_class = FestivalSerializer


# class FestivalDetail(generics.RetrieveAPIView):
#     queryset = Festival.objects.all()
#     serializer_class = FestivalSerializer


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


# class FestivalView(ModelViewSet):
#     queryset = Festival.objects.all()
#     serializer_class = FestivalSerializer
