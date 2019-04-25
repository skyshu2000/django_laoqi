from django.contrib import admin
from .models import BlogArticles

class BlogArticlesAdmin(admin.ModelAdmin):
    # 参考： https://docs.djangoproject.com/zh-hans/2.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    # list_display 用来控制哪些字段会显示在列表中
    # 如果不设置 list_display，列表只会显示数据模型类中 __str__()的字段
    list_display = ("title", "author", "publish")

    # 参考： https://docs.djangoproject.com/zh-hans/2.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    # list_filter 用来控制哪些字段放在过滤器中，并在列表的右侧栏中显示
    list_filter = ("publish", "author")

    # 参考： https://docs.djangoproject.com/zh-hans/2.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
    # search_fields 用来控制哪些字段可以用来字符搜索
    # 在 search_fields 列表中的字段应该是字符型的，例如CharField或者TextField
    # 一旦设置了search_fields，会在列表页上方出现搜索框
    search_fields = ("title", "body")

    # 参考：https://docs.djangoproject.com/zh-hans/2.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.raw_id_fields
    # raw_id_fields 中的字段如果是ForeignKey, 则只显示其在表中的id数值
    # 在不设置 raw_id_fields 的情况下，显示外键对应的表的显示字段
    # 此设置不在列表页体现，而是在编辑页体现
    raw_id_fields = ("author",)

    # 参考：https://docs.djangoproject.com/zh-hans/2.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.date_hierarchy
    # 参考：https://www.jianshu.com/p/36e0f7571815
    date_hierarchy = "publish"

    # 参考：https://docs.djangoproject.com/zh-hans/2.2/ref/contrib/admin/#django.contrib.admin.ModelAdmin.ordering
    # ordering 用来控制列表的排序字段组合
    ordering = ["publish", "author"]


admin.site.register(BlogArticles, BlogArticlesAdmin)
