from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ProfileUpdateForm
from django.contrib.auth import get_user_model

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

