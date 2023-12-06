from django.shortcuts import render, get_object_or_404
from .models import Post, Comment


def index(request):
    post_list = Post.objects.order_by("-create_date")
    context = {"post_list": post_list}
    return render(request, "board/post_list.html", context)

def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'board/post_detail.html', context)