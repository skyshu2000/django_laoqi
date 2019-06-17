from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo


class LoginForm(forms.Form):
    """
    This is for user login form.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")
    
    # def save(self, commit=True):
    #     user = super(UserCreateForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #     return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone", "birth")

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school", "company", "profession", "address", "aboutme")

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)