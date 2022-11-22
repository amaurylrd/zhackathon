from rest_framework.viewsets import ModelViewSet

from .models import Festival
from .serializers import FestivalSerializer


class FestivalView(ModelViewSet):
    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer
