from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'categories',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        if text is not None and len(text) < 300:
            raise ValidationError({'text': 'Объём публикации должен быть не меньше 300 символов!'})

        title = cleaned_data.get('title')
        if title[0].islower():
            raise ValidationError('Название должно начинаться с заглавной буквы!')

        return cleaned_data