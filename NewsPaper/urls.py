from django.urls import path
from .views import PostCreateView, PostDeleteView, PostListView, PostDetailView, PostUpdateView, PostSearchListView, sendmail, subscribe, unsubscribe

urlpatterns = [
    path('', PostListView.as_view(), name='news_list'),
    path('search/', PostSearchListView.as_view(), name='news_search'),
    path('<int:pk>/', PostDetailView.as_view(), name='news_detail'),
    path('add/', PostCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),
    path('subscribe/', subscribe, name='subscribe'),
    path('unsubscribe/', unsubscribe, name='unsubscribe'),
    path('sendmail/', sendmail, name='sendmail')
]