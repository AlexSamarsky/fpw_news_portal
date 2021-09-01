from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render

from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from .models import Category, CategorySubscribers, Post, PostCategory
from NewsPaper.utils import get_external_url

def new_posts():

    print(f'{datetime.now()} begin sending posts')

    now = datetime.now()
    seven_days = timedelta(days=-7)

    date_posts = now + seven_days

    posts = Post.objects.filter(updated__gte=date_posts).values()

    posts_id = []
    # posts = []
    categories_id = []
    for post_model in posts:
        posts_id.append(post_model['id'])
        post_model['post_url'] = f'http://{Site.objects.get_current().domain}:8000/news/{post_model["id"]}'
        # post = {
        #         'id': post_model.id,
        #         't': 1,
        #         }

    post_categories = list(PostCategory.objects.filter(post__in=posts_id).values())
    
    for post_category in post_categories:
        categories_id.append(post_category['category_id'])
    
    subscribers = CategorySubscribers.objects.filter(category__in=categories_id).values('id', 'user_id', 'user__email', 'category_id')
    
    users = set(map(lambda x: x['user_id'], list(subscribers)))
    # users = []
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
                
                # print(message_text)
                if recipients:
                    send_mail('Новые посты',
                                        message_text,
                                        settings.EMAIL_HOST_USER,
                                        recipients,
                                        html_message=message_text
                                    )

            
        
    # context = {
    #     'news': posts
    # }
    
    # # Category.objects.
    # return render(request=request, template_name='mail/new_posts.html', context=context)
    print(f'{datetime.now()} complete sending posts')

def cron_log():
    print('s')