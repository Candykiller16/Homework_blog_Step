from django.shortcuts import render, get_object_or_404

from blog.forms import CommentForm
from blog.models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    page = request.GET.get('page')
    paginator = Paginator(posts.order_by('-id'), 4)
    try:
        # передаем пагинатору page из шаблона
        posts = paginator.page(page)
    except PageNotAnInteger:
        # если что-то пойдет не так, то выведи один
        posts = paginator.page(1)
    except EmptyPage:
        # если в БД пусто, то выведи число страниц
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts': posts,
                                                   'page': page,
                                                   'tag': tag})


def post_detail(request, pk):
    post = get_object_or_404(Post,
                             pk=pk)  # эта строчка. pk = это парметр функции get_object_or_404, а второй pk - это парметр функции post_detail
    comments = post.comments.filter(
        active=True)  # запрос(QuerySet) для получения всех активных комментариев для конкретного поста.
    # строится запрос так: объект post, связанный с моделью Post, далее ис. manager для связи определенный как related_name='comments', и фильтрация для определения активных комментариев
    if request.method == 'POST':  # если же запрос POST
        comment_form = CommentForm(data=request.POST)  # то созд. экземпляр формы с использованием отправных данных
        if comment_form.is_valid():  # проверка с помошью is_valid, если же не прошла проверку, то будут отображаться ошибки валидности в шаблоне
            new_comment = comment_form.save(
                commit=False)  # если она валидная, то 1. созд. новый объект Comment вызвав метод save
            # метод save() созд. экземпляр модели, с которой связана форма и сохр. в БД,
            # commit=False позволяет созд. экземпляр модели, но не сохраняет его в БД, если потребуется изменение
            new_comment.post = post  # связь комментария с конкретным постом
            new_comment.save()  # созраняем комментарий в БД
    else:  # если request.method == 'GET', т.е. мы исп. один и тот же view для отображения формы заполнения комментария
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form})  # 'post' это ключ, по которому осущ запрос на верхней строчке
