from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from .models import Post
import logging
from django.core.management import call_command


# Отправка уведомления о новой публикации
User = get_user_model()


@shared_task
def send_new_post_notifications(post_id):
    try:
        instance = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return f"Post {post_id} not found"

    short_text = (instance.text[:50] + '...') if len(instance.text) > 50 else instance.text
    full_url = f"{settings.SITE_URL}/news/{instance.id}/"

    # Делаем один запрос к категориям, чтобы не спамить БД в цикле
    for category in instance.categories.all():
        subscribers = category.subscribers.filter(
            is_active=True,
            email__isnull=False
        ).exclude(email="")

        if not subscribers.exists():
            continue

        subject = f"Новая публикация в категории '{category.name}': {instance.title}"

        for user in subscribers:
            context = {
                'username': user.username,
                'category_name': category.name,
                'post_title': instance.title,
                'short_text': short_text,
                'full_url': full_url,
                'created_at': instance.created_at.strftime('%Y-%m-%d %H:%M'),  # Сериализуем дату в строку
            }

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

    return f"Notifications for post {post_id} sent successfully"

# Отправка недельного дайджеста
logger = logging.getLogger(__name__)

@shared_task(name="weekly_digest_task")
def weekly_digest_job():
    logger.info("Celery: Запуск еженедельной рассылки дайджеста...")
    try:
        call_command('send_weekly_digest')
        logger.info("Celery: Рассылка дайджеста успешно завершена.")
        return "Дайджест отправлен"
    except Exception as e:
        logger.error(f"Celery: Ошибка при выполнении рассылки: {e}")
        raise e

