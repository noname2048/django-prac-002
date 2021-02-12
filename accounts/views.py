from django.contrib import messages
from django.shortcuts import render, redirect, resolve_url
from django.core.mail import send_mail

from .forms import SignupForm


def root(request):
    return render(request, "accounts/none.html", {})


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save(commit=False)

            messages.success(request, f"Welcome {signed_user.username}")

            if signed_user.send_welcom_email() == 1:  # FIXME: selary 로 하기
                next_url = request.GET.get("next", "/")
                return redirect(next_url)
            else:
                form = SignupForm()
    else:
        form = SignupForm()
    return render(
        request,
        "accounts/signup_form.html",
        {
            "form": form,
        },
    )


def test_mail(request):
    subject = "회원가입을 환영합니다 test"
    content = "환영환영~"
    sender_email = "sungwook.csw@noname2048.dev"
    t = send_mail(subject, content, sender_email, ["sungwook.csw@gmail.com"], fail_silently=False)
    print(t)

    next_url = request.GET.get("next", resolve_url("accounts:root"))
    return redirect(next_url)
