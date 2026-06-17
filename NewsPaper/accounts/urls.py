from django.urls import path
from .views import (
    ProfileUpdateView, upgrade_me,
)
from . import views

urlpatterns = [
    path('edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('subscribe/<int:pk>/', views.toggle_subscription, name='toggle_subscription'),
]
