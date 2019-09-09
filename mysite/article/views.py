from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import ArticleColumn, ArticlePost
from .forms import ArticleColumnForm, ArticlePostForm

@login_required(login_url='/account/built-in-login/')
@csrf_exempt
def article_column(request):
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(
            request,
            "article/column/article_column.html",
            {"columns":columns, "column_form":column_form},
        )
    
    if request.method == "POST":
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id, column=column_name)
        if columns:
            return HttpResponse('2')
        else:
            ArticleColumn.objects.create(user_id=request.user.id, column=column_name)
            return HttpResponse('1')


@login_required(login_url='/account/built-in-login/')
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST["column_name"]
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

@login_required(login_url='/account/built-in-login/')
@require_POST
@csrf_exempt
def delete_article_column(request):
    column_id = request.POST["column_id"]
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='/account/built-in-login/')
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(request.POST)
        if article_post_form.is_valid():
            #cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                #new_article.tags = request.POST("tags")
                new_article.save()
                # Withour this next line, the tags won't be saved
                article_post_form.save_m2m()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        return render(request, "article/column/article_post.html", 
                      {"article_post_form":article_post_form, 
                      "article_columns":article_columns})


from django.views.generic import ListView
class ArticlePostListView(ListView):
    model = ArticlePost
    context_object_name = "articles"
    template_name = "article/column/article_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = ArticlePost.objects.filter(author=self.request.user)
        return queryset



from django.views.generic.detail import DetailView
class ArticlePostDetailView(DetailView):
    model = ArticlePost
    context_object_name = "article"
    template_name = "article/column/article_detail.html"


@login_required(login_url='/account/built-in-login/')
@require_POST
@csrf_exempt
def del_article(request):
    article_id = request.POST['article_id']
    try:
        #article = ArticlePost.get_object_or_404(id=article_id)
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@login_required(login_url='/account/built-in-login/')
@csrf_exempt
def redit_article(request, article_id):
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        article_form = ArticlePostForm(initial={"title":article.title, "body":article.body, "tags":article.tags})
        article_column = article.column
        article_tags = article.tags
        return render(request, 
                      "article/column/redit_article.html", 
                      {"article":article, 
                       "article_columns":article_columns,
                       "article_column":article_column,
                       "article_form":article_form,
                       "article_tags":article_tags,
                      }
                     )
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
               
            return HttpResponse("1")
        except:
            return HttpResponse("2")




