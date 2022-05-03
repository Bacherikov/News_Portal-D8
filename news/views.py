from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post
from .filters import PostFilter  # импортируем недавно написанный фильтр
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin  # 14.2 заменил на PermissionRequiredMixin в PostUpdate
from django.contrib.auth.mixins import PermissionRequiredMixin  # 14.2

class PostsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'posts.html'
    # указываем имя шаблона, где будет лежать HTML, в котором будут все инструкции о том,
    # как именно пользователю должны вывестись наши объекты
    context_object_name = 'posts'
    # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Post.objects.order_by('-create_time')
    paginate_by = 10


class PostDetail(DetailView):
    template_name = 'post.html'
    queryset = Post.objects.all()

class PostsSearchList(ListView):
    model = Post
    template_name = 'news/search/posts_filters.html'
    context_object_name = 'posts'
    ordering = '-create_time'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        # вписываем наш фильтр в контекст
        return context

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'  # 14.2
    template_name = 'news/post_create.html'
    form_class = PostForm


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'  # 14.2
    login_url = '/admin/login/'
    template_name = 'news/post_update.html'
    form_class = PostForm
# метод get_object мы используем вместо queryset,
# чтобы получить информацию об объекте, который мы собираемся редактировать

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'