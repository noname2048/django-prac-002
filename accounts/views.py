from django.contrib import messages
from django.shortcuts import render, redirect, resolve_url
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import SignupForm
from django.contrib.auth import login as auth_login


@login_required
def accounts_root(request):
    return render(request, "accounts/accounts_root.html", {})


class AcountLoginView(LoginView):
    template_name = "accounts/login_form.html"


login = LoginView.as_view(template_name="accounts/login_form.html")


def logout(request):
    messages.success(request, "성공적으로 로그아웃 하였습니다.")
    return logout_then_login(request)


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save(commit=False)

            try:
                signed_user.send_welcom_email()
                signed_user.save()

                messages.success(request, f"{signed_user.username}님의 가입을 환영합니다.")

                auth_login(request, signed_user)

                next_url = request.GET.get("next", "/")
                return redirect(next_url)
            except:
                messages.warning(request, f"이메일 발송에 문제가 있습니다.")
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
