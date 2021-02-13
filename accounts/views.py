from django.contrib import messages
from django.shortcuts import render, redirect, resolve_url
from django.core.mail import send_mail
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .forms import PasswordChangeForm, SignupForm, ProfileForm
from django.contrib.auth import login as auth_login

from django.utils.http import (
    url_has_allowed_host_and_scheme,
    urlsafe_base64_decode,
)

from django.conf import settings
import logging

logger = logging.getLogger("django.server")


@login_required
def accounts_root(request):
    logger.info("logout!")
    return render(request, "accounts/accounts_root.html", {})


class LoginView(auth_views.LoginView):
    template_name = "accounts/login_form.html"


login = LoginView.as_view()


def logout(request):
    messages.success(request, "성공적으로 로그아웃 하였습니다.")
    return auth_views.logout_then_login(
        request, login_url=f'{reverse("accounts:login")}?next={reverse("accounts:root")}'
    )


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


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필을 수정/저장 하였습니다.")
            return redirect("accounts:profile_edit")
    else:
        form = ProfileForm(instance=request.user)
    return render(
        request,
        "accounts/profile_edit_form.html",
        {
            "form": form,
        },
    )


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    success_url = reverse_lazy("accounts:password_change")
    template_name = "accounts/password_change_form.html"
    form_class = PasswordChangeForm

    def form_valid(self, form):
        messages.success(self.request, "암호를 변경했습니다.")
        return super().form_valid(form)


password_change = PasswordChangeView.as_view()
