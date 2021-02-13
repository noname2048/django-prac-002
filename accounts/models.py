from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.loader import render_to_string


class User(AbstractUser):
    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    def send_welcom_email(self):
        subject = "회원가입을 환영합니다 test"
        content = f"{self.username}님의 회원가입을 환영합니다."
        sender_email = settings.DEFAULT_FROM_EMAIL
        return send_mail(subject, content, sender_email, [self.email], fail_silently=False)

    # TODO: POST_SAVE signal
