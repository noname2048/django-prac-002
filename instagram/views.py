from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth import get_user_model, get_user
from .models import Tag


def root(request):
    return render(request, template_name="root.html")


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # post.tag_set
            post.author = get_user(request)
            post.save()
            post.tag_set.add(*post.extract_tag_list())

            messages.success(request, "포스팅을 저장하였습니다.")
            return redirect("instagram:root")
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
