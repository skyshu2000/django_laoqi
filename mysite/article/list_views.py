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


class ArticlePostDetailView(DetailView):
    model = ArticlePost
    context_object_name = "article"
    template_name = "article/list/article_detail.html"