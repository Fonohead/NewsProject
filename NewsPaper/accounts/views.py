from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ProfileUpdateForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Author
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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


# Функция для отправки HTML-письма
def send_welcome_html_mail(user, category_name):
    subject = f"Успешная подписка на категорию '{category_name}'"

    context = {
        'username': user.username,
        'category_name': category_name,
        'site_url': settings.SITE_URL,
    }

    # Рендерим HTML-шаблон и создаем чистый текст для старых клиентов
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


# Подписка на Политика
@login_required
def subscribe_politics(request):
    if request.method == 'POST':
        user = request.user
        politics_group = Group.objects.get(name='sub_politics')
        if not user.groups.filter(name='sub_politics').exists():
            politics_group.user_set.add(user)
            send_welcome_html_mail(user, 'Политика')

    return redirect(request.META.get('HTTP_REFERER', '/'))


# Подписка на Культура
@login_required
def subscribe_culture(request):
    if request.method == 'POST':
        user = request.user
        culture_group = Group.objects.get(name='sub_culture')
        if not user.groups.filter(name='sub_culture').exists():
            culture_group.user_set.add(user)
            send_welcome_html_mail(user, 'Культура')

    return redirect(request.META.get('HTTP_REFERER', '/'))


# Подписка на Спорт
@login_required
def subscribe_sport(request):
    if request.method == 'POST':
        user = request.user
        sport_group = Group.objects.get(name='sub_sport')
        if not user.groups.filter(name='sub_sport').exists():
            sport_group.user_set.add(user)
            send_welcome_html_mail(user, 'Спорт')

    return redirect(request.META.get('HTTP_REFERER', '/'))


# Подписка на Юмор
@login_required
def subscribe_humour(request):
    if request.method == 'POST':
        user = request.user
        humour_group = Group.objects.get(name='sub_humour')
        if not user.groups.filter(name='sub_humour').exists():
            humour_group.user_set.add(user)
            send_welcome_html_mail(user, 'Юмор')

    return redirect(request.META.get('HTTP_REFERER', '/'))


