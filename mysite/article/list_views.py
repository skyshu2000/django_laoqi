from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404,redirect, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import ArticlePost, Comment
from .forms import CommentForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy, reverse


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        obj.update_total_views()            
        context["total_views"] = obj.total_views   

        comments = Comment.objects.filter(article=obj)
        context["comments"] = comments

        return context


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

@login_required(login_url="/account/built-in-login/")
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                
                # 如果回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id

                # 被回复人
                new_comment.reply_to = parent_comment.user

                new_comment.save()
                return HttpResponse('200 OK')
            
            new_comment.save()
            #return redirect(article)
            return HttpResponseRedirect(reverse('article:article_content', 
                    kwargs={'pk':article.id, 'slug':article.slug}))
        else:
            return HttpResponse("表单内容有误，请重新填写！")
    # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'article/list/reply.html', context)
    else:
        return HttpResponse("仅接受GET/POST请求！")


@login_required(login_url="/account/built-in-login/")
def post_comment_reply(request):
    # 处理 POST 请求
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        article = get_object_or_404(ArticlePost, id=article_id)
        comment_form = CommentForm()
        
        new_comment = comment_form.save(commit=False)
        new_comment.article = article
        new_comment.user = request.user
        new_comment.body = request.POST.get('body')

        parent_comment_id = request.POST.get('parent_comment_id')
        # 二级回复
        if parent_comment_id:            
            parent_comment = Comment.objects.get(id=parent_comment_id)
            
            # 如果回复层级超过二级，则转换为二级
            new_comment.parent_id = parent_comment.get_root().id

            # 被回复人
            new_comment.reply_to = parent_comment.user

            new_comment.save()
            return HttpResponse('200 OK')
        else:   
            return HttpResponse("表单内容有误，请重新填写！")
        
    else:
        return HttpResponse("仅接受POST请求")