from django.contrib import admin
from .models import ArticlePost

class ArticlePostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "column", "created")
    raw_id_fields = ("author",)


admin.site.register(ArticlePost, ArticlePostAdmin)
