from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm, PostEditForm
from .models import Post
from django.shortcuts import render, redirect
from .filters import NewsFilter
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def home(request):
    return render(request, 'flatpages/main.html')

def search(request):
    return render(request, 'flatpages/post_search.html')

# Список публикаций
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

# Детальный вид публикации
class PostDetailView(DetailView):
    model = Post
    template_name = 'flatpages/post_detail.html'
    context_object_name = 'post'


# Страница поиска новости
def news_search(request):
    news_list = Post.objects.all().select_related('author__user')  # ← Оптимизация: загружаем сразу User
    news_filter = NewsFilter(request.GET, queryset=news_list)

    paginator = Paginator(news_filter.qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'flatpages/post_search.html', {
        'filter': news_filter,
        'page_obj': page_obj,
    })


# Форма создания статьи
class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = False
    model = Post
    form_class = PostForm
    template_name = 'flatpages/articles/article_edit.html'
    success_url = reverse_lazy('news:post_list')

    def handle_no_permission(self):
        return redirect('news:access_denied')

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        form.instance.post_type = 'AR'
        return super().form_valid(form)

# Редактирование статьи
class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    raise_exception = False
    model = Post
    form_class = PostEditForm
    template_name = 'flatpages/articles/article_edit.html'
    success_url = reverse_lazy('news:post_list')

    def handle_no_permission(self):
        return redirect('news:editing_denied')

    def dispatch(self, request, *args, **kwargs):
        # Получаем объект статьи до начала обработки запроса
        obj = self.get_object()

        # Проверяем тип контента
        if obj.post_type != 'AR':
            raise Http404("Это не статья!")

        # Проверяем автора статьи
        if obj.author.user != request.user:
            return self.handle_no_permission()

        # Если все проверки пройдены, продолжаем стандартную работу UpdateView
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Возвращаем метод к его первоначальному виду
        return super().get_object(queryset)

# Форма создания новости
class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = False
    model = Post
    form_class = PostForm
    template_name = 'flatpages/post_edit.html'
    success_url = reverse_lazy('news:post_list')

    def handle_no_permission(self):
        return redirect('news:access_denied')

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        form.instance.post_type = 'NW'
        return super().form_valid(form)

# Редактирование новости
class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    raise_exception = False
    model = Post
    form_class = PostEditForm
    template_name = 'flatpages/post_edit.html'
    success_url = reverse_lazy('news:post_list')

    def handle_no_permission(self):
        return redirect('news:editing_denied')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.post_type != 'NW':
            raise Http404("Это не новость!")
        if obj.author.user != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super().get_object(queryset)

# Удаление статьи
class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    raise_exception = False
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('news:post_list')

    def handle_no_permission(self):
        return redirect('news:access_denied')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.post_type != 'AR':
            raise Http404("Это не статья!")
        if obj.author.user != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super().get_object(queryset)

# Удаление новости
class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    raise_exception = False
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('news:post_list')

    def handle_no_permission(self):
        return redirect('news:editing_denied')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.post_type != 'NW':
            raise Http404("Это не новость!")
        if obj.author.user != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return super().get_object(queryset)

@login_required
def access_denied(request):
    return render(request, 'flatpages/access_denied.html')

@login_required
def editing_denied(request):
    return render(request, 'flatpages/editing_denied.html')



