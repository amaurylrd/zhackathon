from rest_framework.serializers import ModelSerializer

from zhackathon.models import Festival


class FestivalSerializer(ModelSerializer):
    class Meta:
        model = Festival
        fields = (
            "identifiant",
            # "name", fields = '__all__'
            # "description",
            # "start_date",
            # "end_date",
            # "location",
            # "website",
            # "logo",
            # "banner",
            # "created_at",
            # "updated_at",
            # "deleted_at",
        )
