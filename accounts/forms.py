from django import forms
from django.contrib.auth import forms as auth_forms
from .models import User


class SignupForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields["email"].required)
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일 주소입니다.")
            return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "avatar",
            "first_name",
            "last_name",
            "website_url",
            "bio",
            "phone_number",
            "gender",
        ]


class PasswordChangeForm(auth_forms.PasswordChangeForm):
    def clean_new_password1(self):
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password1")

        if old_password == new_password1:
            raise forms.ValidationError("새로운 암호는 기존 암호와 다르게 입력해주세요")
        return new_password1
