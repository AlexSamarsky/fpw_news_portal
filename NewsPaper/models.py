from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render

news = 'NW'
article = 'ART'

PostTypes = [
    (news, 'news'),
    (article, 'article'),
]

class Category(models.Model):
    ''' Категории
    '''
    name = models.CharField(max_length=150, unique=True, verbose_name='Наименование')

    def __str__(self):
        str = f'{self.name}'
        return str


class Author(models.Model):
    ''' Авторы статей
    метод обновления рейтинга - считается на основании активности автора
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор', primary_key=True)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def __str__(self):
        str = f'{self.user.username} / rating: {self.rating}'
        return str

    @staticmethod
    def update_rating(user_name):
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist as e:
            print('unknown user')
            return
        
        author = Author.objects.get(user=user)
        post_rating = Post.objects.filter(author=author).aggregate(total=Sum('rating'))
        user_rating = Comment.objects.filter(user=user).aggregate(total=Sum('rating'))
        post_comments_rating = Comment.objects.filter(post__author=author).exclude(user=user).aggregate(total=Sum('rating'))

        author.rating = post_rating['total'] * 3 + user_rating['total'] + post_comments_rating['total']
        author.save()


class Post(models.Model):
    ''' Статья/Новость
    '''
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    type = models.CharField(max_length=3, choices=PostTypes, default=article, verbose_name='Тип сообщения', null=True)
    updated = models.DateTimeField(auto_now_add=True, verbose_name='Дата обновления')
    title = models.CharField(max_length=250, verbose_name='Название', null=True)
    text = models.TextField(verbose_name='Текст', null=True)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    
    categories = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    
    def __str__(self):
        str = f'{self.updated:%Y-%m-%d %H:%M} - author: {self.author.user.username} / title: {self.title} // {self.preview()}'
        return str
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) < 124:
            return self.text
        else:
            return f'{self.text[:124]}...'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class Comment(models.Model):
    ''' Комментарии к статьям
    '''
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Сообщение')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст', null=True)
    updated = models.DateTimeField(auto_now_add=True, verbose_name='Дата обновления')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    
    def __str__(self):
        str = f'{self.updated:%Y-%m-%d %H:%M} - user: {self.user.username} / rating: {self.rating} // {self.text}'
        return str
    
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Сообщение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')


class CategorySubscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

