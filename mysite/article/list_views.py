from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import ArticlePost
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


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


@csrf_exempt
@require_POST
@login_required(login_url="/account/built-in-login/")
def like_article(request):
    article_id = request.POST.get("id")
    action = request.POST.get("action")
    if article_id and action:
        try:
            article = ArticlePost.objects.get(id=article_id)
            if action == "like":
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no")