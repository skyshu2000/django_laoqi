from django.urls import path
from . import views

app_name = "article"

urlpatterns = [
    # 创建栏目
    path('article-column/', views.article_column, name="article_column"),

    # 修改栏目名称
    path('rename-column/', views.rename_article_column, name="rename_article_column"),

    # 删除栏目
    path('delete-column/', views.delete_article_column, name="delete_article_column"),

    # 创建文章
    path('article-post/', views.article_post, name="article_post"),

    # 文章列表
    path('article-list/', views.ArticlePostListView.as_view(), name="article_list"),

    # 文章详情
    path('article-detail/<int:pk>/<slug>/', views.ArticlePostDetailView.as_view(), name="article_detail"),

    # 删除文章
    path('del-article/', views.del_article, name="del_article"),

    # 编辑文章
    path('redit-article/<int:article_id>/', views.redit_article, name="redit_article"),
]