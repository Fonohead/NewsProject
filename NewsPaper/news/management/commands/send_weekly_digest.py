from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from datetime import timedelta
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Отправляет еженедельный дайджест новых статей всем подписчикам категорий'

    def handle(self, *args, **options):
        # 1. Вычисляем временную метку ровно 7 дней назад
        one_week_ago = timezone.now() - timedelta(days=7)

        # 2. Получаем абсолютно все категории, у которых есть хотя бы один подписчик
        categories = Category.objects.filter(subscribers__isnull=False).distinct()

        if not categories.exists():
            self.stdout.write(self.style.WARNING("На сайте пока нет категорий с активными подписчиками."))
            return

        # 3. Проходим циклом по каждой обитаемой категории
        for category in categories:

            # Находим все посты этой категории, созданные за последние 7 дней
            weekly_posts = Post.objects.filter(
                categories=category,
                created_at__gte=one_week_ago
            ).distinct()

            # Если за неделю в категории не появилось ни одной статьи, дайджест не отправляем
            if not weekly_posts.exists():
                continue

            # Получаем список всех активных пользователей, подписанных на данную категорию
            subscribers = category.subscribers.filter(is_active=True, email__isnull=False).exclude(email="")

            if not subscribers.exists():
                continue

            # Генерируем полные абсолютные URL-адреса для каждого поста
            for post in weekly_posts:
                post_id = str(post.id)
                post.full_url = f"{settings.SITE_URL}/news/{post_id}/"

            # Перебираем подписчиков по одному для персональной отправки
            for user in subscribers:
                # Получаем имя (или username, если имя не заполнено)
                username = user.first_name if user.first_name else user.username

                # Добавляем имя пользователя в контекст шаблона
                context = {
                    'username': username,
                    'category_name': category.name,
                    'posts': weekly_posts,
                }

                # Рендерим шаблон индивидуально для каждого пользователя
                html_content = render_to_string('emails/weekly_digest.html', context)
                text_content = strip_tags(html_content)
                subject = f"Еженедельный дайджест в категории '{category.name}'"

                # Отправляем конкретному пользователю
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email]  # Отправка строго одному адресату
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=True)

            self.stdout.write(self.style.SUCCESS(
                f"Дайджесты по категории '{category.name}' успешно отправлены ({subscribers.count()} шт.)."))

