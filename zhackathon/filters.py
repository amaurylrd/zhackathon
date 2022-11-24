from django_filters import filterset
from rest_framework import filters

from . import models


class CommentFilterSet(filterset.FilterSet):
    class Meta:
        model = models.Comment
        fields = ["festival"]
