from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from accounts.models import Author


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

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.get_or_create(user=user)
    return redirect('/')
