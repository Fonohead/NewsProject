from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm, PostEditForm
from .models import Post, Category
from .filters import NewsFilter
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.exceptions import ValidationError

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

# Список публикаций Политика

class PoliticsListView(PostListView):
    template_name = 'flatpages/posts_politics.html'

    def get_queryset(self):
        # 1. Получаем ID из URL-пути
        category_id = self.kwargs.get('category_id')
        # 2. Проверяем существование категории
        category = get_object_or_404(Category, id=category_id)
        # 3. Фильтруем базовый queryset модели Post
        queryset = Post.objects.filter(categories=category).order_by('-created_at')

        # 4. Применяем фильтрацию NewsFilter поверх выбранной категории
        self.filterset = NewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # 1. Сначала вызываем базовый контекст родительского класса
        context = super().get_context_data(**kwargs)

        # 2. Снова безопасно берем category_id из URL конкретно для контекста
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)

        # 3. Передаем точное количество публикаций текущей категории (с учетом фильтров)
        context['total_posts'] = self.get_queryset().count()

        # 4. Передаем объект категории для вывода её названия в HTML
        context['current_category'] = category

        return context

# Список публикаций Культура

class CultureListView(PostListView):
    template_name = 'flatpages/posts_culture.html'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        queryset = Post.objects.filter(categories=category).order_by('-created_at')
        self.filterset = NewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        context['total_posts'] = self.get_queryset().count()
        context['current_category'] = category

        return context

# Список публикаций Спорт

class SportListView(PostListView):
    template_name = 'flatpages/posts_sport.html'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        queryset = Post.objects.filter(categories=category).order_by('-created_at')
        self.filterset = NewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        context['total_posts'] = self.get_queryset().count()
        context['current_category'] = category

        return context

# Список публикаций Юмор

class HumourListView(PostListView):
    template_name = 'flatpages/posts_humour.html'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        queryset = Post.objects.filter(categories=category).order_by('-created_at')
        self.filterset = NewsFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, id=category_id)
        context['total_posts'] = self.get_queryset().count()
        context['current_category'] = category

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
    model = Post
    form_class = PostForm
    template_name = 'flatpages/articles/article_edit.html'
    success_url = reverse_lazy('news:post_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'request': self.request}  # Передаем объект запроса в форму
        return kwargs


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
    model = Post
    form_class = PostForm
    template_name = 'flatpages/post_edit.html'  # ваш шаблон для новостей
    success_url = reverse_lazy('news:post_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'request': self.request}  # Передаем объект запроса в форму
        return kwargs


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


# Подписка на любую категорию
@login_required
def toggle_subscription(request, pk):
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=pk)
        user = request.user

        # Если пользователя нет в подписчиках, то подписываем
        if not category.subscribers.filter(id=user.id).exists():
            category.subscribers.add(user)

            # Отправка приветственного HTML-письма
            subject = f"Успешная подписка на категорию '{category.name}'"
            context = {
                'username': user.username,
                'category_name': category.name,
                'site_url': settings.SITE_URL,
            }
            html_content = render_to_string('emails/welcome_subscription.html', context)
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)

    return redirect(request.META.get('HTTP_REFERER', '/'))





