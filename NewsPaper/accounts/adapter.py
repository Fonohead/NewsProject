
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        # Сначала даем allauth создать и сохранить пользователя стандартным путем
        user = super().save_user(request, sociallogin, form)

        # Получаем или создаем группу 'common'
        group, _ = Group.objects.get_or_create(name='common')

        # Добавляем пользователя в группу
        user.groups.add(group)

        return user
