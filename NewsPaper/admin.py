from django.contrib import admin
from django.db import models
from .models import Post, Category
# Register your models here.

admin.site.register(Post)
admin.site.register(Category)