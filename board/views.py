from django.shortcuts import render
from .models import Post, Comment


def index(request):
    post_list = Post.objects.order_by("-create_date")
    context = {"post_list": post_list}
    return render(request, "board/post_list.html", context)
