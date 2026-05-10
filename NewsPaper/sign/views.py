from django.contrib.auth.models import User
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
