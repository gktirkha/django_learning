from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'updated_on', 'created_on']
    search_fields = ['title']


admin.site.register(Article, ArticleAdmin)
