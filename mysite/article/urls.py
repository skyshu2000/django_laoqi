from django.urls import path
from . import views, list_views

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

    # 文章列表，只能看到作者自己的文章
    path('article-list/', views.ArticlePostListView.as_view(), name="article_list"),

    # 文章详情
    path('article-detail/<int:pk>/<slug>/', views.ArticlePostDetailView.as_view(), name="article_detail"),

    # 删除文章
    path('del-article/', views.del_article, name="del_article"),

    # 编辑文章
    path('redit-article/<int:article_id>/', views.redit_article, name="redit_article"),

    # 文章列表，可以看到所有作者的文章
    path('list-article-titles/', list_views.ArticleTitlesListView.as_view(), name="article_titles"),

    # 查看文章内容
    path('article-content/<int:pk>/<slug>/', list_views.ArticlePostDetailView.as_view(), name="article_content"),

    # 文章列表，某一用户的全部文章列表
    path('list-article-titles/<username>/', 
         list_views.AuthorArticleTitlesListView.as_view(),
         name="author_articles"),
    
    # 为文章点赞
    path('like-article/', list_views.like_article, name="like_article"),

    # 处理一级回复
    path('post-comment/<int:article_id>/', list_views.post_comment, name='post_comment'),

    # 处理二级回复
    path('post-comment/<int:article_id>/<int:parent_comment_id>/', list_views.post_comment, name='comment_reply'),

    # 处理二级回复
    path('post-comment-reply/', list_views.post_comment_reply, name="post_comment_reply"),
]