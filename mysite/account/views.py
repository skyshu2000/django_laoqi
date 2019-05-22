from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .forms import LoginForm

def user_login(request):
    """
    This view function is for handling user login.

    If request method is 'Get', the login form is provided.

    Otherwise, the request method is 'POST', this funciton will handling the 
    posted login data.
    """
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "login.html", {"form":login_form})
    
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                msg = "Welcom {0}, you have been authenticated sucessfully.".format(username) 
                #return HttpResponse(msg)
            else:
                msg = "Login data is not right! Username:{0};password:{1}".format(username, password)
                #return HttpResponse(msg)
            
            return HttpResponse(msg)
        else:
            return HttpResponse("Invalid login!")


class UserCreateView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('account:built_in_login')
    template_name = 'registration.html'
