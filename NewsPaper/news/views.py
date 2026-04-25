from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm
from .models import Post
from django.shortcuts import render
from .filters import NewsFilter
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.http import Http404

def home(request):
    return render(request, 'flatpages/main.html',)

def search(request):
    return render(request, 'flatpages/post_search.html')

class PostListView(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'flatpages/posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['total_posts'] = Post.objects.count()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'flatpages/post_detail.html'
    context_object_name = 'post'


# Страница поиска новости
def news_search(request):
    news_list = Post.objects.all().select_related('author__user')  # ← Оптимизация: загружаем сразу User
    news_filter = NewsFilter(request.GET, queryset=news_list)

    paginator = Paginator(news_filter.qs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'flatpages/post_search.html', {
        'filter': news_filter,
        'page_obj': page_obj,
    })


# Форма создания статьи
class ArticleCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'flatpages/articles/article_edit.html'
    success_url = '/news/'

    def form_valid(self, form):
        form.instance.post_type = 'AR'
        return super().form_valid(form)

# Редактирование статьи
class ArticleUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'flatpages/articles/article_edit.html'
    success_url = '/news/'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.post_type != 'AR':
            raise Http404("Это не статья!")
        return obj

# Форма создания новости
class NewsCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'flatpages/post_edit.html'
    success_url = '/news/'

    def form_valid(self, form):
        form.instance.post_type = 'NW'
        return super().form_valid(form)

# Редактирование новости
class NewsUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'flatpages/post_edit.html'
    success_url = reverse_lazy('news:post_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.post_type != 'NW':
            raise Http404("Это не новость!")
        return obj

# Удаление статьи
class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('news:post_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.post_type != 'AR':
            raise Http404("Это не статья!")
        return obj

# Удаление новости
class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('news:post_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.post_type != 'NW':
            raise Http404("Это не новость!")
        return obj


