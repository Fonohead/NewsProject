from django.urls import path
from .views import ProfileUpdateView

urlpatterns = [
    path('edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]
