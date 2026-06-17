from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'categories',
            'text',
        ]
        labels = {
            'title': 'Название публикации:',
            'categories': 'Категория:',
            'text': 'Текст публикации:',
        }
        widgets = {
            'title': forms.TextInput(attrs={'size': 40}),
            'category': forms.Select(attrs={'class': 'form_control', 'size': 1}),
            'text': forms.Textarea(attrs={'cols': 100, 'rows': 10}),
        }

    def clean_title(self):
        data = self.cleaned_data['title']
        return data

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')
        if title and title[0].islower():
            raise ValidationError('Название должно начинаться с заглавной буквы!')

        text = cleaned_data.get('text')
        if text is not None and len(text) < 300:
            raise ValidationError({'text': 'Объём публикации должен быть не меньше 300 символов!'})

        # Ограничение до 3 материалов в сутки
        # Извлекаем request, переданный из метода get_form_kwargs во views.py
        request = self.initial.get('request')

        if request and request.user.is_authenticated:
            try:
                # Находим профиль автора у текущего пользователя
                author = request.user.author

                # Вычисляем временную отметку ровно 24 часа назад
                one_day_ago = timezone.now() - timedelta(days=1)

                # Считаем количество постов автора за сутки
                total_publications_24h = Post.objects.filter(
                    author=author,
                    created_at__gte=one_day_ago
                ).count()

                # Если лимит превышен, добавляем общую ошибку формы (non_field_errors)
                if total_publications_24h >= 3:
                    self.add_error(
                        None,
                        "Вы не можете публиковать более 3 материалов (статей или новостей) в сутки. "
                        "Пожалуйста, подождите."
                    )
            except Exception:
                # Если у пользователя нет связанного профиля автора, просто пропускаем проверку
                pass

        return cleaned_data


# Редактирование публикации
class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'categories',
            'text',
        ]
        labels = {
            'title': 'Название публикации:',
            'categories': 'Категория:',
            'text': 'Текст публикации:',
        }
        widgets = {
            'title': forms.TextInput(attrs={'size': 40}),
            'category': forms.Select(attrs={'class': 'form_control', 'size': 1}),
            'text': forms.Textarea(attrs={'cols': 100, 'rows': 10}),
        }

    def clean_title(self):
        data = self.cleaned_data['title']
        return data

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        if text is not None and len(text) < 300:
            raise ValidationError({'text': 'Объём публикации должен быть не меньше 300 символов!'})

        title = cleaned_data.get('title')
        if title[0].islower():
            raise ValidationError('Название должно начинаться с заглавной буквы!')

        return cleaned_data