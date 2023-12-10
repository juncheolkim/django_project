from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import Post
from django.db.models import Q


def index(request):
    page = request.GET.get("page", "1")  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    post_list = Post.objects.order_by("-create_date")

    if kw:
        # subject__contains=kw 대신 subject__icontains=kw을 사용하면 대소문자를 가리지 않고 찾아 준다.
        post_list = post_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(comment__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(comment__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    paginator = Paginator(post_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {"post_list": page_obj, 'page': page, 'kw': kw}
    return render(request, "board/post_list.html", context)


def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {"post": post}
    return render(request, "board/post_detail.html", context)
