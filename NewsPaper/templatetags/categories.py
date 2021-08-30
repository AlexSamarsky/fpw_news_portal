# <app>/templatetags/categories.py
from dataclasses import dataclass
from NewsPaper.models import CategorySubscribers
from django import template
from django.template.loader import get_template
import re

register = template.Library()

@dataclass
class PostCategory:
    id: int
    name: str
    is_subscribed: bool


@register.simple_tag(takes_context=True)
def categories(context, value):
    template_category = get_template('category.html')
    
    if context.request.user.is_anonymous:
        user_subscribe_categories = []
    else:
        user_subscribe_categories = CategorySubscribers.objects.filter(user=context.request.user)

    post_categories = list(value.all())
    list_categories = []
    for post_category in post_categories:
        is_subscribed = True if list(filter(lambda x: x.category == post_category, list(user_subscribe_categories))) else False
        
        new_post_category = PostCategory(post_category.id, post_category.name, is_subscribed)
        list_categories.append(new_post_category)

    content = {
        'categories': list_categories,
        'request': context.get('request')
    }
    return template_category.render(content)