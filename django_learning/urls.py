from django.contrib import admin
from django.urls import path
from .views import *
from articles import views

urlpatterns = [
    path('', home_view),
    path('admin/', admin.site.urls),
    path('articles/', views.article_search_view),
    path('articles/create/', views.article_create_view),
    path('articles/<int:id>', views.article_detail_view),

]
