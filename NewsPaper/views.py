from typing import Any, Dict
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse

from .forms import PostForm, PostFormCreate
from .filters import PostFilter
from .models import Post


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
    paginate_by = 1
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
