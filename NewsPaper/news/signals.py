from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import Group
from django.conf import settings
from .models import Post

# Отправка письма новому подписчику
@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":

        CATEGORY_GROUPS = {
            'Культура': 'sub_culture',
            'Политика': 'sub_politics',
            'Спорт': 'sub_sport',
            'Юмор': 'sub_humour',
        }

        for category in instance.categories.all():
            group_name = CATEGORY_GROUPS.get(category.name)

            if group_name:
                try:
                    group = Group.objects.get(name=group_name)
                    subscribers = group.user_set.filter(is_active=True, email__isnull=False).exclude(email="")
                except Group.DoesNotExist:
                    continue

                if not subscribers.exists():
                    continue

                # Подготовка данных для письма
                subject = f"Новая публикация в категории '{category.name}': {instance.title}"
                short_text = instance.preview()
                post_id = str(instance.id)
                full_url = f"http://127.0.0.1:8000/news/{post_id}/"

                # Контекст для передачи переменных внутрь HTML-шаблона
                context = {
                    'category_name': category.name,
                    'post_title': instance.title,
                    'short_text': short_text,
                    'full_url': full_url,
                    'created_at': instance.created_at,
                }

                html_content = render_to_string('emails/new_post_notification.html', context)
                text_content = strip_tags(html_content)
                recipient_list = [user.email for user in subscribers]

                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=recipient_list
                )

                msg.attach_alternative(html_content, "text/html")

                msg.send(fail_silently=True)
