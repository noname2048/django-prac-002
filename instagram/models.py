from django.db import models
from django.conf import settings
from django.urls import reverse
import re


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(models.Model):
    # date 기본 정보
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # post 핵심기능
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="my_post_set",  # user.my_post_set
    )
    photo = models.ImageField(upload_to="instagram/post/%Y/%m/%d")
    caption = models.TextField(max_length=500)
    location = models.CharField(max_length=100)

    # tag 관련
    tag_set = models.ManyToManyField("Tag", blank=True)

    # 좋아요 기능
    like_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="like_post_set",  # user.like_post_set
    )

    def __str__(self):
        return self.caption

    @property
    def author_name(self):
        return f"{self.author.name}"

    def get_absolute_url(self):
        return reverse("instagram:post_detail", kwargs={"pk": self.pk})

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.caption)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)

        return tag_list

    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()

    class Meta:
        ordering = ["-id"]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
