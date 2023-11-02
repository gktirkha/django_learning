from django.contrib import admin
from django.urls import path
from .views import home_view
from articles import views as article
from accounts import views as accounts

urlpatterns = [
    path('', home_view),
    path('admin/', admin.site.urls),

    # For Articles
    path('articles/', article.article_search_view),
    path('articles/create/', article.article_create_view),
    path('articles/<int:id>', article.article_detail_view),

    # For accounts
    path('login/', accounts.login_view),
    path('logout/', accounts.logout_view),

]
