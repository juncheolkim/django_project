from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..models import Post, Comment
from ..forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
            return redirect('{}#comment_{}'.format(
                resolve_url('board:detail', post_id=post.id), comment.id))
    else:
        return redirect("board:detail", post_id=post.id)
    context = {"post": post, "form": form}
    return render(request, "board/post_detail.html", context)


@login_required(login_url="common:login")
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "수정권한이 없습니다")
        return redirect("board:detail", post_id=comment.post.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('board:detail', post_id=comment.post.id), comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {"comment": comment, "form": form}
    return render(request, "board/comment_form.html", context)


@login_required(login_url="common:login")
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "삭제권한이 없습니다")
    else:
        comment.delete()
    return redirect("board:detail", post_id=comment.post.id)


@login_required(login_url='common:login')
def comment_vote(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        comment.voter.add(request.user)
    return redirect('{}#comment_{}'.format(
                resolve_url('board:detail', post_id=comment.post.id), comment.id))