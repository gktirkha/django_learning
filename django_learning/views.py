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
    query_set = Article.objects.all()
    context['my_list'], context['qs'], context["article_obj"] = my_list, query_set, article

    HTML_STRING = render_to_string("home_view.html", context=context)
    return HttpResponse(HTML_STRING)
