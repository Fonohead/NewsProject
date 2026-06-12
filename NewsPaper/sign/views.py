from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import logout


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = reverse_lazy('login')

def logout_user(request):
    logout(request)
    return redirect('/')

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
    return context



