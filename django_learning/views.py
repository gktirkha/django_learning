from django.template.loader import render_to_string
from articles.models import Article
from django.http import HttpResponse
from django.shortcuts import render


def home_view(request):
    context = {}
    article = None

    try:
        article = Article.objects.get(id=1)
    except:
        article = None

    my_list = [1, 2, 3, 4, 5, 6]
    url_list = [
        {"name": "admin panel", "url": "/admin/"},
        {"name": "Create Article", "url": "/articles/create/"},
        {"name": "Article Details", "url": "/articles/1"},
        {"name": "Login", "url": "/login/"},
        {"name": "Logout", "url": "/logout/"},
    ]
    query_set = Article.objects.all()
    context['my_list'], context['qs'], context["article_obj"], context['url_list'] = my_list, query_set, article, url_list

    HTML_STRING = render_to_string("home_view.html", context=context)
    return HttpResponse(HTML_STRING)
