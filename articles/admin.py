from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'title', 'updated_on', 'created_on']
    search_fields = ['title', 'slug']
    raw_id_fields=['user']


admin.site.register(Article, ArticleAdmin)
