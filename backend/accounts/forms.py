from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(UserCreationForm):
    name = forms.CharField(
        label=_("Full Name"),
        widget=forms.TextInput(),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(),
    )
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(),
    )
    country = forms.CharField(
        required=False,
        widget=forms.TextInput(),
    )

    class Meta:
        model = User
        fields = ["name", "email", "password1", "password2", "country"]

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get("name", "").strip()
        parts = full_name.split(" ", 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ""
        user.country = self.cleaned_data.get("country")
        if commit:
            user.save()
        return user