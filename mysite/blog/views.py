from django.shortcuts import render
from .models import BlogArticles

def blog_title(request):
    blogs = BlogArticles.objects.all()
    return render(request, "blog/titles.html", {"blogs":blogs})

def blog_article(request, article_id):
    article = BlogArticles.objects.get(id=article_id)
    return render(request, "blog/content.html", {"article":article})