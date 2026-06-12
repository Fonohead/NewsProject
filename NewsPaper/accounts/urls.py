from django.urls import path
from .views import (
    ProfileUpdateView, upgrade_me,
    subscribe_politics, subscribe_culture,
    subscribe_sport, subscribe_humour,
)

urlpatterns = [
    path('edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('subscribe_politics/', subscribe_politics, name='sub_politics'),
    path('subscribe_culture/', subscribe_culture, name='sub_culture'),
    path('subscribe_sport/', subscribe_sport, name='sub_sport'),
    path('subscribe_humour/', subscribe_humour, name='sub_humour'),
]
