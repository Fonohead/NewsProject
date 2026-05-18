from django.urls import path
from .views import PostListView, PostDetailView, news_search
from . import views

app_name = 'news'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', news_search, name='news_search'),
    path('access-denied/', views.access_denied, name='access_denied'),
    path('editing-denied', views.editing_denied, name='editing_denied'),
]