from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import *




class PostFilter(FilterSet):
    Category = ModelChoiceFilter(lookup_expr='exact',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='Any'
        )


    added_after = DateTimeFilter(
        field_name="date",
        lookup_expr='gt',
        widget=DateTimeInput(
        format='%Y-%m-%dT%H:%M',
        attrs={'type': 'datetime-local'},
        ),)


    class Meta:
            model = Post
            fields = {'title': ['icontains']}