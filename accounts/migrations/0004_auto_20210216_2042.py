# Generated by Django 3.1.5 on 2021-02-16 20:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='follower_set',
            field=models.ManyToManyField(blank=True, related_name='following_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='48px * 48px 크기의 png/jpg 파일을 업로드 해주세요.', upload_to='accounts/profile/%y/%m/%d/%S'),
        ),
    ]