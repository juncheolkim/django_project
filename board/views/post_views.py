from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..models import Post
from ..forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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


@login_required(login_url="common:login")
def post_modify(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, "수정권한이 없습니다")
        return redirect("board:detail", post_id=post.id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.modify_date = timezone.now()  # 수정일시 저장
            post.save()
            return redirect("board:detail", post_id=post.id)
    else:
        form = PostForm(instance=post)
    context = {"form": form}
    return render(request, "board/post_form.html", context)


@login_required(login_url="common:login")
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, "삭제권한이 없습니다")
        return redirect("board:detail", post_id=post.id)
    post.delete()
    return redirect("board:index")


@login_required(login_url='common:login')
def post_vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        # voter는 여러사람을 추가할 수 있는 ManyToManyField이므로 add 함수를 사용하여 추천인을 추가한다.
        # 중복 추가는 ManyToManyField 내부에서 자체적으로 처리돼서 적용되지 않는다.
        post.voter.add(request.user)
    return redirect('board:detail', post_id=post.id)