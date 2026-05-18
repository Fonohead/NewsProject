
from django.dispatch import receiver
from django.contrib.auth.models import Group
from allauth.account.signals import user_signed_up


@receiver(user_signed_up)
def add_new_social_user_to_group(request, user, **kwargs):
    """
    Вызывается, когда пользователь успешно зарегистрировался
    как через обычную форму, так и через соцсети (Google, Yandex).
    """
    # Получаем или создаем группу 'common'
    group, _ = Group.objects.get_or_create(name='common')

    # Добавляем пользователя в группу
    user.groups.add(group)

    # КРИТИЧЕСКИ ВАЖНО: Явно принудительно сохраняем инстанс пользователя,
    # чтобы зафиксировать изменения связей в БД после выполнения allauth.
    user.save()
