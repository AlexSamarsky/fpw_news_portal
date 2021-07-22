from django.contrib.auth.models import User
from NewsPaper.models import Author, Category, Comment, Post, PostCategory
user1 = User.objects.create_user('Ivanov', password='foo')
user2 = User.objects.create_user('Petrov', password='boo')
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)
category1 = Category.objects.create(name='Sport')
category2 = Category.objects.create(name='Economy')
category3 = Category.objects.create(name='Astronomy')
category4 = Category.objects.create(name='Pets')

post1 = Post.objects.create(author=author1, type='ART', title='World record in dogs jumping', text='this is ever high dog jump')
post1_category4 = PostCategory.objects.create(post=post1, category=category4)
post1_category1 = PostCategory.objects.create(post=post1, category=category1)

post2 = Post.objects.create(author=author2, type='ART', title='Black hole', text='first photo of black hole')
post2_category3 = PostCategory.objects.create(post=post2, category=category3)

news1 = Post.objects.create(author=author1, type='NW', title='Englan champion', text='England win UEFA Europe Championship')
news1_category1 = PostCategory.objects.create(post=news1, category=category1)

post1_comment1 = Comment.objects.create(user=user1, post=post1, text='comment')
post1_comment2 = Comment.objects.create(user=user2, post=post1, text='new comment')
post2_comment1 = Comment.objects.create(user=user1, post=post2, text='cool')
news1_comment1 = Comment.objects.create(user=user2, post=news1, text='fantastic')

post1_comment1.like()
post1_comment2.like()
post1_comment2.like()
post1_comment2.like()
post1_comment2.like()
post1.like()
post1.like()
post1.like()
post1.like()
post2.like()
post2.like()
news1.like()
post2_comment1.like()
post1_comment2.dislike()

Author.update_rating('Petrov')
Author.update_rating('Ivanov')

print(Author.objects.all().order_by('-rating')[0])

rated_post = Post.objects.all().order_by('-rating')[0]
print(rated_post)

print(Comment.objects.filter(post=rated_post).all())