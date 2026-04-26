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
        labels = {
            'author': 'Автор (выберите из списка):',
            'title': 'Название публикации:',
            'categories': 'Категория:',
            'text': 'Текст публикации:',
        }
        widgets = {
            'author': forms.Select(attrs={'class': 'form_control'}),
            'title': forms.TextInput(attrs={'size': 40}),
            'category': forms.Select(attrs={'class': 'form_control', 'size': 1}),
            'text': forms.Textarea(attrs={'cols': 100, 'rows': 10}),
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        if text is not None and len(text) < 300:
            raise ValidationError({'text': 'Объём публикации должен быть не меньше 300 символов!'})

        title = cleaned_data.get('title')
        if title[0].islower():
            raise ValidationError('Название должно начинаться с заглавной буквы!')

        return cleaned_data