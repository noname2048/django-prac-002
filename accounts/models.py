from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.loader import render_to_string
from django.core.validators import RegexValidator
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, Thumbnail


class User(AbstractUser):
    class GenderInGender(models.TextChoices):
        MAIL = "M", "남"
        FEMAILE = "F", "여"

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        validators=[RegexValidator(r"^01\d-?\d{3,4}-?\d{4}$")],
    )
    gender = models.CharField(
        max_length=5,
        blank=True,
        choices=GenderInGender.choices,
    )
    avatar = models.ImageField(
        blank=True,
        upload_to="accounts/profile/%y/%m/%d/%S",
        help_text="48px * 48px 크기의 png/jpg 파일을 업로드 해주세요.",
    )
    avatar_thumbnail = ImageSpecField(
        # upload_to="accounts/profile/%y/%m/%d/%S_thumnail",
        source="avatar",
        processors=[ResizeToFill(50, 50)],
        format="JPEG",
        options={"quality": 100},
    )

    def send_welcom_email(self):
        subject = "회원가입을 환영합니다 test"
        content = f"{self.username}님의 회원가입을 환영합니다."
        sender_email = settings.DEFAULT_FROM_EMAIL
        return send_mail(subject, content, sender_email, [self.email], fail_silently=False)

    # TODO: POST_SAVE signal
