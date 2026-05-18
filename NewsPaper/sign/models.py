from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django import forms
from allauth.account.forms import SignupForm

# Форма регистрации через логин.
class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email:')
    first_name = forms.CharField(label='Имя:')
    last_name = forms.CharField(label='Фамилия:')
    password1 = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Пароль повторно:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )

        labels = {
            'username': 'Логин:',
        }

# Автоматически добавляет пользователя в группу common.
class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user