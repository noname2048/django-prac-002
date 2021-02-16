from django.contrib.auth import login
from django.shortcuts import get_object_or_404, render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth import get_user_model, get_user
from .models import Tag, Post
import logging

logger = logging.getLogger("django.server")


def root(request):
    return render(request, template_name="root.html")


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
    return render(
        request,
        "instagram/post_detail.html",
        {
            "post": post,
        },
    )


def user_page(request, username):
    page_user = get_object_or_404(get_user_model(), username=username, is_active=True)
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
        },
    )
