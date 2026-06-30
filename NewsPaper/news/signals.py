# Оповещение о новой публикации
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post
from .tasks import send_new_post_notifications

@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, **kwargs):
    # Запускаем задачу только после того, как связи m2m успешно добавлены в БД
    if action == "post_add":
        send_new_post_notifications.delay(instance.id)
