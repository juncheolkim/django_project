from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


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


# request.user에는 로그아웃 상태이면 AnonymousUser 객체가, 로그인 상태이면 User 객체가 들어있다.
# @login_required 애너테이션이 붙은 함수는 로그인이 필요한 함수를 의미한다.
@login_required(login_url="common:login")
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # author 속성에 로그인 계정 저장
            comment.create_date = timezone.now()
            comment.post = post
            comment.save()
            return redirect("board:detail", post_id=post.id)
    else:
        return redirect("board:detail", post_id=post.id)
    context = {"post": post, "form": form}
    return render(request, "board/post_detail.html", context)


@login_required(login_url="common:login")
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # author 속성에 로그인 계정 저장
            post.create_date = timezone.now()
            post.save()
            return redirect("board:index")
    else:
        form = PostForm()
    context = {"form": form}
    return render(request, "board/post_form.html", context)
