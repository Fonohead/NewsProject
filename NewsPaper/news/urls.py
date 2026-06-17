from multiprocessing.managers import public_methods

from django.urls import path
from .views import (
    PostListView, PostDetailView, news_search,
    PoliticsListView, CultureListView,
    SportListView, HumourListView
)
from . import views

app_name = 'news'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('search/', news_search, name='news_search'),
    path('access-denied/', views.access_denied, name='access_denied'),
    path('editing-denied', views.editing_denied, name='editing_denied'),
    path('politics/<int:category_id>/', PoliticsListView.as_view(), name='post_politics'),
    path('culture/<int:category_id>/', CultureListView.as_view(), name='post_culture'),
    path('sport/<int:category_id>/', SportListView.as_view(), name='post_sport'),
    path('humour/<int:category_id>/', HumourListView.as_view(), name='post_humour'),
    path('subscribe/<int:pk>/', views.toggle_subscription, name='toggle_subscription'),

]