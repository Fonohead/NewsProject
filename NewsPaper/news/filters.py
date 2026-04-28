from dataclasses import field

import django_filters
from .models import Post
from django import forms

# Фильтр поиска публикации
class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='iregex',
        label='Название новости:',
        widget=forms.TextInput()
    )

    author__user__username = django_filters.CharFilter(
        lookup_expr='iregex',
        label='Имя автора:',
        widget=forms.TextInput()
    )

    created_at_gt = django_filters.DateFilter(
        field_name='created_at__date',
        lookup_expr='gt',
        label='Опубликовано позже даты:',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'style': 'width: 300px',
                'placeholder': 'ГГГГ-ММ-ДД',
                'font': 'color: grey',
            }
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'created_at_gt']


