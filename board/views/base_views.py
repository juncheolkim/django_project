from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import Post


def index(request):
    page = request.GET.get("page", "1")  # 페이지
    post_list = Post.objects.order_by("-create_date")
    paginator = Paginator(post_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {"post_list": page_obj}
    return render(request, "board/post_list.html", context)


def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {"post": post}
    return render(request, "board/post_detail.html", context)
