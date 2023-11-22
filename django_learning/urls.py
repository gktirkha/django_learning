from django.contrib import admin
from django.urls import path, include
from .views import home_view
from accounts import views as accounts

urlpatterns = [
    path('', home_view),
    path('admin/', admin.site.urls),

    # For Articles
    path('articles/', include('articles.urls')),

    # For accounts
    path('login/', accounts.login_view),
    path('logout/', accounts.logout_view),
    path('signup/', accounts.signup_view),

]
