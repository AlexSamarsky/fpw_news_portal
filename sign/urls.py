from django.urls import path
from .views import be_author, permissions

urlpatterns = [
    path('be_author/', be_author, name='be_author'),
    path('permissions/', permissions, name='permissions'),
]

