from django.contrib import admin
from django.db import models
from django.http.request import HttpRequest
from .models import Author, Post, Category
# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Author)

class PostAdmin(admin.ModelAdmin):

    

    def has_add_permission(self, request: HttpRequest, obj) -> bool:
        if obj is None:
            return False
        if request.user.is_super_user():
            return True
        elif request.user == obj.author.user:
            return True
        else:
            return False
        # return super().has_add_permission(request)