from django import forms
from .models import ArticleColumn, ArticlePost, Comment
from taggit.forms import TagWidget

class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ('column',)

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost        
        fields = ("title", "body", "tags",)
        widgets = {
            'tags': TagWidget(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
