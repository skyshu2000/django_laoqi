from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = "account"

urlpatterns = [
    # 自定义登录方法的路由
    path('login/', views.user_login, name="user_login"),

    # 使用内置的LoginView类处理登录的路由
    path('built-in-login/', LoginView.as_view(template_name='built_in_login.html'), name='built_in_login'),

    # 使用内置的LogoutView类处理登出的路由
    path('built-in-logout/', LogoutView.as_view(next_page='/blog/'), name='built_in_logout'),  

    # 用户注册处理路由
    path('registration/', views.UserCreateView.as_view(), name='registration'),  

    # 用户注册处理路由，在注册中添加email，并创建user profile的关联use_id 
    path('registration2/', views.UserRegistrationView.as_view(), name="registration2"),
]