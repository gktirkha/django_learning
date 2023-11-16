from django.shortcuts import render
from .models import Article
from django.http import HttpRequest, Http404
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm


def article_detail_view(request: HttpRequest, slug):
    article_obj = None
    try:
        article_obj = Article.objects.get(slug=slug)

    except Article.DoesNotExist:
        raise Http404

    except Article.MultipleObjectsReturned:
        article_obj = Article.objects.filter(slug=slug).first()

    except:
        raise Http404

    context = {'article_obj': article_obj}
    return render(request=request, template_name='articles/details.html', context=context)


def article_search_view(request: HttpRequest):
    context = {}
    query = request.GET['q']
    qs = Article.objects.all().search(query=query)
    context['article_list'] = qs

    return render(request=request, context=context, template_name='articles/search.html')


@login_required
def article_create_view(request: HttpRequest):
    form = ArticleForm(request.POST or None)
    context = {'form': form}

    if (request.method == 'POST'):
        if form.is_valid():
            article_obj = form.save()
            context['article_obj'], context['created'] = article_obj,  True

    return render(request=request, context=context, template_name='articles/create.html')
