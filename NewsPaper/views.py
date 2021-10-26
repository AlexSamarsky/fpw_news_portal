from typing import Any, Dict
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from django.template.loader import render_to_string

from .utils import get_external_url
from .forms import PostForm, PostFormCreate
from .filters import PostFilter
from .models import Category, CategorySubscribers, Post

from .tasks import send_email_message

import logging

class FilteredListView(ListView):
    filterset_class = None
    form_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
        context['form'] = self.form_class()
        return context

class PostListView(FilteredListView):
    filterset_class = PostFilter
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    recordset = Post.objects.order_by('-id').all()
    paginate_by = 2
    # ordering = ['id', 'author__user__username']
    form_class = PostForm

    def get_ordering(self):
        return self.request.GET.get('ordering')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_exists = self.request.user.groups.filter(name = 'authors').exists()
        context['is_not_author'] = not author_exists
        context['is_author'] = author_exists
        return context
    # http_method_names = ['GET', 'POST']
    
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
            
    #     return super().get(request, *args, **kwargs)


class PostSearchListView(PostListView):
    template_name = 'news_search.html'
    


class PostDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()
    context_object_name = 'new'
    
    def get_context_data(self, **kwargs):

        logger.error('test')

        context = super().get_context_data(**kwargs)

        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)
        can_edit = False
        if self.request.user.is_superuser:
            can_edit = True
        elif self.request.user == post.author.user:
            can_edit = True

        context['can_edit'] = can_edit
        return context

class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news_create.html'
    form_class = PostFormCreate
    permission_required = ('NewsPaper.add_post')

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial.update({ 'created_by': self.request.user })
        return initial

    def __init__(self) -> None:
        super().__init__()
        pass

    def form_valid(self, form) -> HttpResponse:
        form_redirect = super().form_valid(form)
        
        if form.is_valid():
            post = form.save()
            external_url = get_external_url(self.request, form_redirect.url)

            recipients = list(
                                CategorySubscribers.objects\
                                    .filter(category__in=form.cleaned_data['categories'])\
                                    .exclude(user=self.request.user)\
                                    .values_list('user__email', flat=True)
                            )

            send_email_message.delay(post.id, external_url, recipients)
            
        return form_redirect
    
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPaper.change_post')
    template_name = 'news_create.html'
    form_class = PostForm
    
    def get_object(self, **kwargs):

        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)
        if id is None:
            return Post.objects.get(pk=0)
        if self.request.user.is_superuser:
            return post
        elif self.request.user == post.author.user:
            return post
        else:
            return Post.objects.get(pk=0)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPaper.delete_post')
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'new'

    def get_object(self, **kwargs):

        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)
        if id is None:
            return Post.objects.get(pk=0)
        if self.request.user.is_superuser:
            return post
        elif self.request.user == post.author.user:
            return post
        else:
            return Post.objects.get(pk=0)

@login_required
def subscribe(request):
    try:
        category_id = int(request.GET['category'])
        category = Category.objects.get(id=category_id)
        if not CategorySubscribers.objects.filter(user = request.user, category = category).exists():
            category_subscriber = CategorySubscribers(user = request.user, category = category)
            category_subscriber.save()
    except:
        pass
    finally:
        return HttpResponseRedirect(f'/news/?{request.META["QUERY_STRING"]}')


@login_required
def unsubscribe(request):
    try:
        category_id = int(request.GET['category'])
        category = Category.objects.get(id=category_id)
        if CategorySubscribers.objects.filter(user = request.user, category = category).exists():
            category_subscriber = CategorySubscribers.objects.get(user = request.user, category = category)
            category_subscriber.delete()
    except:
        pass
    finally:
        return HttpResponseRedirect(f'/news/?{request.META["QUERY_STRING"]}')


def sendmail(request):
    check = send_mail('Тема', 'Тело письма', settings.EMAIL_HOST_USER, ['xsami@yandex.ru'])
    return HttpResponseRedirect(f'/news/?{request.META["QUERY_STRING"]}')
