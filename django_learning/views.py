from django.template.loader import render_to_string
from articles.models import Article
from django.http import HttpResponse


def home_view(request):
    article = Article.objects.get(id=2)
    my_list = [1, 2, 3, 4, 5, 6]
    query_set = Article.objects.all()
    print(query_set)
    context = {"title": article.title,
               "content": article.content,
               "id": article.id,
               "my_list": my_list,
               'qs': query_set
               }
    HTML_STRING = render_to_string("home_view.html", context=context)
    return HttpResponse(HTML_STRING)
