from django.shortcuts import render, get_object_or_404

from blog.forms import CommentForm
from blog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts.order_by('-id'), 4)

    page = request.GET.get('page')

    try:
        # передаем пагинатору page из шаблона
        posts = paginator.page(page)
    except PageNotAnInteger:
        # если что-то пойдет не так, то выведи один
        posts = paginator.page(1)
    except EmptyPage:
        # если в БД пусто, то выведи число страниц
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts': posts, 'page': page})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) # эта строчка. pk = это парметр функции get_object_or_404, а второй pk - это парметр функции post_detail
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments':comments, 'comment_form':comment_form}) # 'post' это ключ, по которому осущ запрос на верхней строчке

