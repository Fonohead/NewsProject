import django_filters
from .models import Post
from django import forms

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название новости:',
        widget=forms.TextInput()
    )

    author__user__username = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Имя автора:',
        widget=forms.TextInput()
    )

    created_at__gt = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='Опубликованно позже даты:',
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
        fields = ['title', 'author__user__username', 'created_at__gt']


