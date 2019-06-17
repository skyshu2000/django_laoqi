from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "account"

urlpatterns = [
    # 自定义登录方法的路由
    path('login/', views.user_login, name="user_login"),

    # 使用内置的LoginView类处理登录的路由
    path('built-in-login/', auth_views.LoginView.as_view(template_name='built_in_login.html'), name='built_in_login'),

    # 使用内置的LogoutView类处理登出的路由
    path('built-in-logout/', auth_views.LogoutView.as_view(next_page='/blog/'), name='built_in_logout'),  

    # 用户注册处理路由
    path('registration/', views.UserCreateView.as_view(), name='registration'),  

    # 用户注册处理路由，在注册中添加email，并创建user profile的关联use_id 
    path('registration2/', views.UserRegistrationView.as_view(), name="registration2"),

    # 用户修改密码路由
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html', success_url="/account/password-change-done/"), name="password_change"),

    # 用户修改密码完成路由
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name="password_change_done"),

    # 发起密码重置流程
    path(
        'password-reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='password_reset_form.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt',
            success_url='/account/password-reset/done/'
        ), 
        name='password_reset'
    ),
    
    # 密码重置提交完成
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # 处理重置密码令牌
    path(
        'password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html',
            success_url='/account/password-reset/complete/'
        ),
        name='password_reset_confirm'
    ),

    # 密码重置完成
    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # 显示用户信息
    path('my-info/', views.myself, name="my_info"),
]