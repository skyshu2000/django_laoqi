from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import ArticlePost


class ArticleTitlesListView(ListView):
    model = ArticlePost
    context_object_name = "articles"
    template_name = "article/list/article_titles.html"
    paginate_by = 4

    def get_queryset(self):
        queryset = ArticlePost.objects.all()
        return queryset

class AuthorArticleTitlesListView(ListView):
    model = ArticlePost
    context_object_name = "articles"
    template_name = "article/list/author_articles.html"
    paginate_by = 2

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username']) 
        queryset = ArticlePost.objects.filter(author=self.user)
        return queryset

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        self.author = get_object_or_404(User, username=self.kwargs['username']) 
        context['userinfo'] = self.author.userinfo
        context['author'] = self.author
        return context


class ArticlePostDetailView(DetailView):
    model = ArticlePost
    context_object_name = "article"
    template_name = "article/list/article_detail.html"