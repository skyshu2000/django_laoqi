from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from .models import UserProfile, UserInfo
from .forms import LoginForm, UserCreateForm, UserProfileForm
from .forms import UserInfoForm, UserForm


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

class UserRegistrationView(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('account:built_in_login')
    template_name = 'registration2.html'

    def form_valid(self, form):
        new_user = UserCreateForm(self.request.POST).save()
        # new_user_form = UserCreateForm(self.request.POST)
        # new_user = new_user_form.save(commit=False)
        # new_user.email = new_user_form.cleaned_data['email']
        # new_user.save()

        new_user_profile = UserProfileForm().save(commit=False)
        new_user_profile.user = new_user
        new_user_profile.save()    

        UserInfo.objects.create(user=new_user)

        return HttpResponseRedirect(reverse('account:built_in_login'))

@login_required(login_url='/account/built-in-login/')
def myself(request):
    user = User.objects.get(username=request.user.username)

    if hasattr(user, 'userprofile'):
        userprofile = UserProfile.objects.get(user=user)
    else:
        userprofile = UserProfile.objects.create(user=user)
    
    if hasattr(user, 'userinfo'):
        userinfo = UserInfo.objects.get(user=user)
    else:
        userinfo = UserInfo.objects.create(user=user)
    
    return render(request, 'myself.html', 
                  {"user":user, "userprofile":userprofile, 
                  "userinfo":userinfo}
                 )

@login_required(login_url='/account/built-in-login/')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)

    if hasattr(user, 'userprofile'):
        userprofile = UserProfile.objects.get(user=user)
    else:
        userprofile = UserProfile.objects.create(user=user)
    
    if hasattr(user, 'userinfo'):
        userinfo = UserInfo.objects.get(user=user)
    else:
        userinfo = UserInfo.objects.create(user=user)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)

        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data

            user.email = user_cd['email']

            userprofile.birth = userprofile_cd['birth']
            userprofile.phone = userprofile_cd['phone']

            userinfo.school = userinfo_cd['school']
            userinfo.company = userinfo_cd['company']
            userinfo.profession = userinfo_cd['profession']
            userinfo.address = userinfo_cd['address']
            userinfo.aboutme = userinfo_cd['aboutme']

            user.save()
            userprofile.save()
            userinfo.save()

        return HttpResponseRedirect('/account/my-info/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(
            initial={
                "birth":userprofile.birth, 
                "phone":userprofile.phone}
        )
        userinfo_form = UserInfoForm(
            initial={
                "scholl":userinfo.school,
                "company":userinfo.company, 
                "profession":userinfo.profession, 
                "address":userinfo.address, 
                "aboutme":userinfo.aboutme
            }
        )
        return render(request, 
                      "myself_edit.html", 
                      {"user_form":user_form, 
                       "userprofile_form":userprofile_form, 
                       "userinfo_form":userinfo_form
                      }
                     )