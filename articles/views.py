from django.shortcuts import render
from .models import Article


def article_detail_view(request, id):
    article_obj = None
    if id == None:
        article_obj = Article.objects.get(id=1)
    else:
        article_obj = Article.objects.get(id=id)

    context = {'article_obj': article_obj}
    return render(request=request, template_name='articles/details.html', context=context)
