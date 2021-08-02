from django_filters import FilterSet, widgets
from django_filters.filters import CharFilter, DateFromToRangeFilter, ModelChoiceFilter
from .models import Category, Post, Author
from django import forms


class PostFilter(FilterSet):
    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        # widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    title = CharFilter(lookup_expr='contains', label='Название')
    updated = DateFromToRangeFilter(
        widget=widgets.DateRangeWidget(
            attrs={
                'type': 'date'
            }
        )
    )
    categories = ModelChoiceFilter(queryset=Category.objects.all())
    
    class Meta:
        model = Post
        fields = {
            # 'title': ['icontains'],
            # 'updated': ['gt'],
            # 'author': ['in'],
            # 'categories': ['in'],
        }