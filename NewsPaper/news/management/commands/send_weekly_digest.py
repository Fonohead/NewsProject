from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import Group
from django.conf import settings
from datetime import timedelta
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Отправляет еженедельный дайджест новых статей подписчикам категорий'

    def handle(self, *args, **options):
        # 1. Вычисляем дату ровно неделю назад
        one_week_ago = timezone.now() - timedelta(days=7)

        CATEGORY_GROUPS = {
            'Культура': 'sub_culture',
            'Политика': 'sub_politics',
            'Спорт': 'sub_sport',
            'Юмор': 'sub_humour',
        }

        # Перебираем все категории из нашего списка
        for category_name, group_name in CATEGORY_GROUPS.items():
            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                continue

            # Находим все посты этой категории, созданные за последние 7 дней
            weekly_posts = Post.objects.filter(
                categories=category,
                created_at__gte=one_week_ago
            ).distinct()

            # Если новых статей в этой категории за неделю нет, пропускаем рассылку
            if not weekly_posts.exists():
                continue

            try:
                group = Group.objects.get(name=group_name)
                subscribers = group.user_set.filter(is_active=True, email__isnull=False).exclude(email="")
            except Group.DoesNotExist:
                continue

            if not subscribers.exists():
                continue

            # Добавляем для каждого поста полную ссылку (для использования в шаблоне)
            for post in weekly_posts:
                post.full_url = f"{settings.SITE_URL}/news/{post.id}/"

            # Контекст для HTML-шаблона
            context = {
                'category_name': category_name,
                'posts': weekly_posts,
            }

            # Рендерим HTML и создаем текстовую копию писем
            html_content = render_to_string('emails/weekly_digest.html', context)
            text_content = strip_tags(html_content)
            subject = f"Еженедельный дайджест новых публикаций в категории '{category_name}'"

            # Собираем адреса почты всех подписчиков этой группы
            recipient_list = [user.email for user in subscribers]

            # Отправляем письмо
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recipient_list
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)

            self.stdout.write(self.style.SUCCESS(f"Дайджест по категории '{category_name}' успешно отправлен."))
