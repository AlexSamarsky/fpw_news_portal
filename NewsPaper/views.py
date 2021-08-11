from django.views.generic.edit import DeleteView, UpdateView
from .forms import PostForm
from .filters import PostFilter
from django.views.generic import ListView, DetailView, CreateView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView


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

class PostCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'news_create.html'
    form_class = PostForm
    
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'new'

class PortalLoginView(LoginView):
    template_name = 'login.html'