from django.db import models
from django.utils import timezone


class Article(models.Model):
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
