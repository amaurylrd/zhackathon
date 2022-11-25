from django_filters import filterset

from . import models


class CommentFilterSet(filterset.FilterSet):
    class Meta:
        model = models.Comment
        fields = ["festival"]


class RatingFilterSet(filterset.FilterSet):
    class Meta:
        model = models.Rating
        fields = ["festival"]
