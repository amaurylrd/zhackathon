from django_filters import filterset
from rest_framework import filters

from . import models


class CommentFilterSet(filterset.FilterSet):
    class Meta:
        model = models.Comment
        fields = ["festival"]


class CommentSearchFilter(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)

        if not search_terms and not request.query_params:
            return queryset.none()

        return super().filter_queryset(request, queryset, view)
