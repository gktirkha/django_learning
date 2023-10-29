from django.template.loader import render_to_string
from articles.models import Article
from django.http import HttpResponse


def home_view(request):
    article = Article.objects.get(id=2)
    context = {"title": article.title,
               "content": article.content,
               "id": article.id, }
    HTML_STRING = render_to_string("home_view.html", context=context)
    return HttpResponse(HTML_STRING)
