from NewsPaper.models import Post
from typing import List
from celery import shared_task
import time

from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render

from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from .models import CategorySubscribers, Post, PostCategory

@shared_task
def new_posts(obj):

    print(f'{datetime.now()} begin sending posts')

    now = datetime.now()
    seven_days = timedelta(days=-7)

    date_posts = now + seven_days

    posts = Post.objects.filter(updated__gte=date_posts).values()

    posts_id = []
    categories_id = []
    for post_model in posts:
        posts_id.append(post_model['id'])
        post_model['post_url'] = f'http://{Site.objects.get_current().domain}:8000/news/{post_model["id"]}'

    post_categories = list(PostCategory.objects.filter(post__in=posts_id).values())
    
    for post_category in post_categories:
        categories_id.append(post_category['category_id'])
    
    subscribers = CategorySubscribers.objects.filter(category__in=categories_id).values('id', 'user_id', 'user__email', 'category_id')
    
    users = set(map(lambda x: x['user_id'], list(subscribers)))
    for user_id in users:
        user_categories = []
        email = ''
        for subscriber in subscribers:
            if subscriber['user_id'] == user_id:
                email = subscriber['user__email']
                user_categories.append(subscriber['category_id'])
        
        if email == 'xsami@yandex.ru':
            user_posts_id = []
            for post_category in post_categories:
                if post_category['category_id'] in user_categories:
                    user_posts_id.append(post_category['post_id'])
            user_posts_id = set(user_posts_id)
            
            user_posts = []
            for user_post_id in user_posts_id:
                for post in posts:
                    if post['id'] == user_post_id:
                        user_posts.append(post)

            if user_posts:
                message_text = render_to_string('mail/new_posts.html', { 'news': user_posts, })
                
                recipients = [email]
                
                if recipients:
                    send_mail('Новые посты',
                                        message_text,
                                        settings.EMAIL_HOST_USER,
                                        recipients,
                                        html_message=message_text
                                    )

    print(f'{datetime.now()} complete sending posts')

def cron_log():
    print('s')


@shared_task
def slip(n):
    time.sleep(1)
    for i in range(n):
        print(f'step {i}')
        time.sleep(1)
    print('finish')
    
@shared_task
def send_email_message(post_id: int, post_url: str, recipients: List[str]):
    try:
        
        data = Post.objects.get(id=post_id)
        message_text = render_to_string('mail/new_post.html', { 'new': data, 'post_url': post_url, })
        recipients = set(recipients)
        
        if recipients:
            # print(message_text)
            send_mail('Новый пост',
                                message_text,
                                settings.EMAIL_HOST_USER,
                                recipients,
                                html_message=message_text
                            )
    except:
        pass