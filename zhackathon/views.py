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
from .filters import CommentFilterSet, CommentSearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import GenericViewSet

from django.contrib.auth.models import User


class CommentViewSet(ListCreateAPIView, UpdateAPIView, DestroyAPIView, GenericViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, CommentSearchFilter]
    filterset_class = CommentFilterSet
    search_fields = ["festival"]
    ordering_fields = ["created_at", "updated_at"]

    # TODO mettre ovveride create avec if
    # TODO tester nos if dans put, patch, delete

    def put(self, request, *args, **kwargs):
        if request.data.get("author") == self.request.user:
            return self.update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        if request.data.get("author") == self.request.user:
            return self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, *args, **kwargs):
        if request.data.get("author") == self.request.user:
            return self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        description="Like comment",
        request=serializers.CommentSerializer,
        responses={
            200: serializers.CommentSerializer,
            403: serializers.CommentSerializer,
            404: serializers.CommentSerializer,
            412: serializers.CommentSerializer,
        },
    )
    @action(detail=True, methods=["GET"])
    def like(self, request, *args, **kwargs):
        self.request.like(self.request.user)

    @extend_schema(
        description="Unlike comment",
        request=serializers.CommentSerializer,
        responses={
            200: serializers.CommentSerializer,
            403: serializers.CommentSerializer,
            404: serializers.CommentSerializer,
            412: serializers.CommentSerializer,
        },
    )
    @action(detail=True, methods=["GET"])
    def unlike(self, request, *args, **kwargs):
        comment = self.queryset.get(id=kwargs["pk"])
        comment.liked_by.remove(request.user)
        comment.save()

        return Response()


#        self.request.unlike(self.request.user)


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
