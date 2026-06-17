from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Post


# Оповещение о новой публикации
@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == "post_add":

        for category in instance.categories.all():
            subscribers = category.subscribers.filter(is_active=True, email__isnull=False).exclude(email="")

            if not subscribers.exists():
                continue

            subject = f"Новая публикация в категории '{category.name}': {instance.title}"

            short_text = (instance.text[:50] + '...') if len(instance.text) > 50 else instance.text
            post_id = str(instance.id)
            full_url = f"{settings.SITE_URL}/news/{post_id}/"

            # Отправляем персональное письмо каждому подписчику
            for user in subscribers:
                context = {
                    'username': user.username,
                    'category_name': category.name,
                    'post_title': instance.title,
                    'short_text': short_text,
                    'full_url': full_url,
                    'created_at': instance.created_at,
                }

                # Рендерим шаблон индивидуально для каждого пользователя
                html_content = render_to_string('emails/new_post_notification.html', context)
                text_content = strip_tags(html_content)

                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=True)