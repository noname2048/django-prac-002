from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import SignupForm


def root(request):
    return render(request, "root.html")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Welcome {user.username}")

            next_url = request.GET.get("next", "/")
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(
        request,
        "accounts/signup_form.html",
        {
            "form": form,
        },
    )
