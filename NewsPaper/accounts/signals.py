from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import Group
from allauth.account.signals import email_confirmed, user_signed_up

# Отправка приветственного письма после регистрации
def send_welcome_html_email(user, email_to):
    subject = f"Регистрация успешно завершена! Добро пожаловать, {user.username}."

    context = {
        'username': user.username,
        'site_url': settings.SITE_URL,
    }

    html_content = render_to_string('emails/welcome_registration.html', context)
    text_content = strip_tags(html_content)  # Текстовая копия для старых почтовых клиентов

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email_to]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=True)


@receiver(email_confirmed)
def handle_email_confirmed(request, email_address, **kwargs):
    """
    Пользователь регистрировался вручную по логину/паролю
    Срабатывает ровно в момент клика по ссылке активации из письма.
    """
    user = email_address.user

    # 1. Выдаем группу common
    try:
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
    except Group.DoesNotExist:
        pass

    # 2. Отправляем приветственное HTML-письмо
    send_welcome_html_email(user, email_address.email)


@receiver(user_signed_up)
def handle_social_signup(request, user, **kwargs):
    """
    Пользователь первый раз вошел через Google или Yandex
    Срабатывает мгновенно при создании аккаунта (так как email уже верифицирован соцсетью).
    """
    # Проверяем, что это действительно регистрация через социальную сеть
    if hasattr(user, 'socialaccount_set') and user.socialaccount_set.exists():

        # Выдаем группу common
        try:
            basic_group = Group.objects.get(name='common')
            basic_group.user_set.add(user)
        except Group.DoesNotExist:
            pass

        # Отправляем приветственное HTML-письмо на почту, полученную от Google/Yandex
        if user.email:
            send_welcome_html_email(user, user.email)
