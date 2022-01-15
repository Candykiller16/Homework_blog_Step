from django.shortcuts import render
from blog.models import Post

def posts(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts':posts})
    # return HttpResponse('Posts')

# def post(request):
#     return HttpResponse('Post')