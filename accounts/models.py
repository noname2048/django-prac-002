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
        content = "환영환영~"
        sender_email = "sungwook@noname2048.dev"
        return send_mail(subject, content, sender_email, [self.email], fail_silently=False)
        pass

    # TODO: POST_SAVE signal
