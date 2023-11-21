from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.conf import settings


class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.get_queryset().none()

        lookups = models.Q(title__icontains=query) | models.Q(
            content__icontains=query)
        return self.filter(lookups)


class ArticleManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return ArticleQuerySet(model=self.model)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    content = models.TextField()

    # it will automatically add the date at which the model was added to database
    created_on = models.DateTimeField(auto_now_add=True)

    # it will automatically add the date at which the model was updated in database
    updated_on = models.DateTimeField(auto_now=True)

    # to get the date time input from user
    #  null = true allows null value
    # blank = true allows blank values
    # default will automatically add the default value

    publish_date = models.DateField(
        auto_now_add=False, auto_now=False, null=True, blank=True, default=timezone.now)

    # adding a slug field
    slug = models.SlugField(blank=True, null=True, unique=True)

    # adding url getter
    def url(self):
        return f'/articles/{self.slug}'

    objects = ArticleManager()


def slugify_instance(instance: Article, save: bool = False):
    slug = slugify(instance.title)
    qs = Article.objects.filter(slug=slug).exclude(id=instance.id)

    if qs.exists():
        slug = f"{slug}-{instance.id}"

    instance.slug = slug

    if save:
        instance.save()

    return instance


def article_pre_save(sender, instance: Article, *args, **kwargs):
    if (instance.slug is None):
        slugify_instance(instance=instance, save=False)


def article_post_save(sender, instance: Article, created, *args, **kwargs):
    if created:
        slugify_instance(instance=instance, save=True)


pre_save.connect(receiver=article_pre_save, sender=Article)
post_save.connect(receiver=article_post_save, sender=Article)
