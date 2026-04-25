from django.urls import path
from .views import PostListView, PostDetailView, news_search

app_name = 'news'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', news_search, name='news_search'),
]