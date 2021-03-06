from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from slugify import slugify
from mdeditor.fields import MDTextField
from taggit.managers import TaggableManager

class ArticleColumn(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='article_column'
        )
    column = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.column


class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, on_delete=models.CASCADE, related_name="article_column")
    #body = models.TextField()
    body = MDTextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(User, related_name="articles_like", blank=True)
    total_views = models.PositiveIntegerField(default=0)
    
    tags = TaggableManager()

    class Meta:
        ordering = ("-created",)
        index_together = (("id", "slug"),)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("article:article_detail", args=[self.id, self.slug])
    
    def get_url_path(self):
        return reverse("article:article_content", args=[self.id, self.slug])

    def update_total_views(self):
        self.total_views = self.total_views + 1
        self.save()
    
from mptt.models import MPTTModel, TreeForeignKey
class Comment(MPTTModel):
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    # 用于mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 记录二级评论回复给谁
    reply_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replyers"
    )

    class MPTTMeta:
        order_insertion_by = ['created']
    
    def __str__(self):
        return self.body[:20]
