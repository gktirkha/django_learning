from django.shortcuts import render
from .models import Article
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required


def article_detail_view(request: HttpRequest, id):
    article_obj = None
    if id == None:
        article_obj = Article.objects.get(id=1)
    else:
        article_obj = Article.objects.get(id=id)

    context = {'article_obj': article_obj}
    return render(request=request, template_name='articles/details.html', context=context)

def article_search_view(request: HttpRequest):
    query = None
    article_obj = None
    context = {}

    try:
        query = request.GET['q']
        query = int(query)
        article_obj = Article.objects.get(id=query)
    except:
        query = None
        article_obj = None
        context['article_obj'] = article_obj

    return render(request=request, context=context, template_name='articles/search.html')

@login_required
def article_create_view(request: HttpRequest):
    context = {}

    if (request.method == 'POST'):
        title = request.POST.get('title')
        content = request.POST.get('content')
        article_obj = Article.objects.create(title=title, content=content)
        context['article_obj'], context['created'] = article_obj,  True

    return render(request=request, context=context, template_name='articles/create.html')
