from django import forms


class LoginForm(forms.Form):
    """
    This is for user login form.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)