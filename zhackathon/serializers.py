from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField
from zhackathon.models import Festival


class FestivalSerializer(ModelSerializer):
    class Meta:
        model = Festival
        fields = "__all__"
