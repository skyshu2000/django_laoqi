from django.urls import path
from . import views


app_name = "blog"

urlpatterns = [
    path('', views.blog_title, name="blog_title"),
    # URL for blog content view
    path('<int:article_id>/', views.blog_article, name="blog_article"),
]