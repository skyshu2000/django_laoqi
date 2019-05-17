from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = "account"

urlpatterns = [
    # 自定义登录方法的路由
    path('login/', views.user_login, name="user_login"),
    # 使用内置的LoginView类处理登录的路由
    path('built-in-login/', LoginView.as_view(template_name='built_in_login.html'), name='built_in_login'),
]