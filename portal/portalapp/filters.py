from django_filters import FilterSet
from .models import Response


class ArticleFilter(FilterSet):
    class Meta:
        model = Response
        fields = {
            'article__title': ['icontains'],
        }
