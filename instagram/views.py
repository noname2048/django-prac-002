from django.contrib.auth import login
from django.shortcuts import get_object_or_404, render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.contrib.auth import get_user_model, get_user
from .models import Tag, Post
from django.db.models import Q
import logging

from datetime import timedelta
from django.utils import timezone

logger = logging.getLogger("django.server")


@login_required
def index(request):

    post_list = (
        Post.objects.all()
        .filter(Q(author__in=request.user.following_set.all()) | Q(author=request.user))
        .filter(created_at__gte=timezone.now() - timedelta(days=3))
    )

    suggested_user_list = (
        get_user_model()
        .objects.all()
        .exclude(pk=request.user.pk)
        .exclude(pk__in=request.user.following_set.all())[:3]
    )
    comment_form = CommentForm()

    return render(
        request,
        "instagram/index.html",
        {
            "suggested_user_list": suggested_user_list,
            "post_list": post_list,
            "comment_form": comment_form,
        },
    )


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        logger.warning(str(request))

        if form.is_valid():
            post = form.save(commit=False)
            # post.tag_set
            post.author = get_user(request)
            post.save()
            post.tag_set.add(*post.extract_tag_list())

            messages.success(request, "포스팅을 저장하였습니다.")
            return redirect(post)
            # return redirect(post)
        else:
            post = PostForm(request.POST, request.FILES)

    else:
        form = PostForm()

    return render(
        request,
        "instagram/post_form.html",
        {
            "form": form,
        },
    )


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()

    return render(
        request,
        "instagram/post_detail.html",
        {
            "post": post,
            "comment_form": comment_form,
        },
    )


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)

    if request.user.is_authenticated:
        is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    else:
        is_follow = False

    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count()  # 실제 데이터베이스에 count 쿼리
    # len(post_list_count) 쓰지 마세요

    return render(
        request,
        "instagram/user_page.html",
        {
            "page_user": page_user,
            "post_list": post_list,
            "post_list_count": post_list_count,
            "is_follow": is_follow,
        },
    )


def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, f"좋아요를 눌렀습니다. #post-{post.pk}")
    return redirect(request.META.get("REFFERER", "root"))


def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f"좋아요를 취소했습니다. #post-{post.pk}")
    return redirect(request.META.get("REFFERER", "root"))


@login_required
def comment_new(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            if request.is_ajax():
                return render(
                    request,
                    "instagram/_comment.html",
                    {
                        "comment": comment,
                    },
                )

            return redirect(comment.post)
    else:
        form = CommentForm()

    return render(
        request,
        "instagram/comment_form.html",
        {
            "form": form,
        },
    )
