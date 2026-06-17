from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ProfileUpdateForm
from django.contrib.auth import get_user_model
from .models import Author
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from news.models import Category

# Редактирование профиля автора
User = get_user_model()

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'flatpages/profile/profile_edit.html'
    success_url = reverse_lazy('home')

    # Пользователь может редактировать только свой профиль
    def get_object(self, queryset=None):
        return self.request.user

# Апгрейд до Автора
@login_required
def upgrade_me(request):
    if request.method == 'POST':
        user = request.user
        authors_group = Group.objects.get(name='authors')
        if not user.groups.filter(name='authors').exists():
            authors_group.user_set.add(user)
            Author.objects.get_or_create(user=user)

    # Возвращает пользователя строго на ту страницу, где он нажал кнопку
    return redirect(request.META.get('HTTP_REFERER', '/'))


# Функция подписки на любую категорию публикаций
@login_required
def toggle_subscription(request, pk):
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=pk)
        user = request.user

        # Если пользователь уже подписан — отписываем, если нет — подписываем
        if category.subscribers.filter(id=user.id).exists():
            category.subscribers.remove(user)
        else:
            category.subscribers.add(user)

            # Отправка приветственного HTML-письма
            subject = f"Успешная подписка на категорию '{category.name}'"
            context = {
                'username': user.username,
                'category_name': category.name,
                'site_url': settings.SITE_URL,
            }
            html_content = render_to_string('emails/welcome_subscription.html', context)
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)

    return redirect(request.META.get('HTTP_REFERER', '/'))


