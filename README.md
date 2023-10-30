# Django learning

This readme contains steps that I have done to make project reach here

> This project uses old version of django as I am learning from old book / tutorial

> I am using vs code as my IDE

prerequisites
1. knowledge of creating and activating venv
1. knowledge of pip commands

# Creating venv
1. open your project folder in vscode
1. in your project root run ```python -m venv .venv```
1. close all vscode terminal
1. press ctrl+shift+p and search Python:select interpreter and select .venv from it
1. open vscode terminal ```(.venv)``` before directory name should indicate that python interpreter is changed successfully

# Installing Django
run pip install "Django>=3.2,<3.3" to install django

# Creating requirements.txt
this file is used to store name of packages that we have installed to make the project, it also store dependencies that automatically gets installed while we install a package to make requirements.txt run
```
pip freeze > requirements.txt
```

# Installing packages from requirements.txt
run 
```
pip install -r requirements.txt
```

# creating django project 
```
django-admin startproject <your project name> .
```
> . at the end of the command indicates current directory, you may replace it the directory where you want to create django project

if done correctly following will be the directory structure
> for future reference name of my project is ```django_learning```

```
.
├── manage.py
├── .venv
├── requirements.txt
└── django_learning
    ├── asgi.py
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

# Running Server
to start debug server run 
```
python manage.py reserver
```

it will give following output 

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
October 14, 2023 - 05:39:48
Django version 3.2.22, using settings 'django_learning.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

hit the url in response (http://127.0.0.1:8000/) to view the django web page

> to stop server press ctrl + c

# Resolving  warning 
to resolve
```
You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
```

run 
```
python manage.py migrate
```

# Changing home page (HelloWorld)
1. inside your project folder (django_learning) in my case, create views.py

1. inside views .py add following 
```
from django.http import HttpResponse
def home_view(request):
    return HttpResponse("<h1>Hello World</h1>")
```
3. inside django_learning/urls.py
    - import home_view by ```from .views import home_view```
    - in urlpatterns list add ```path('',view=home_view)```
    - it would look like
        ```
        from django.contrib import admin
        from django.urls import path
        from .views import home_view

        urlpatterns = [
        path('admin/', admin.site.urls),
        path('',view=home_view)
        ]
        ```

1. refresh web page and you should see hello world

# Creating modules
1. run ```django-admin startapp <module name>``` (article in my case)
1. in INSTALLED_APPS in django_learning/settings.py list, add your app name
    ```
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'articles', # add here
    ]
    ```

# Creating models
1. in articles/models.py (replace article with module name) create class that extends ```models.Model```
1. add fields in class <br/>
    for example
    ```
    from django.db import models
    class Article(models.Model):
        title = models.TextField()
        content = models.TextField()
    ```

1. run 
    ```
    python manage.py makemigrations
    python manage.py migrate 
    ```

# Saving Models to storage for feature use
1. run ```python manage.py shell```, it will open django python shell
1. in shell run
    ```
    from articles.models import Article
    obj = Article.objects.create(title="title", content="content")
    obj.save()
    obj.id
    ```
    in the end program will return object id (usually it will be 1)

2. in feature we will do it programmatically, this is up until then

# Creating web template
1. create a folder called template in root of your project
1. create base.html
1. create home_view.html <br/>
    folder will look like
    ```
    .
    ├── articles
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   ├── models.py
    │   ├── __pycache__
    │   ├── tests.py
    │   └── views.py
    ├── db.sqlite3
    ├── manage.py
    ├── README.md
    ├── requirements.txt
    ├── django_learning
    │   ├── asgi.py
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── settings.py
    │   ├── urls.py
    │   ├── views.py
    │   └── wsgi.py
    └── templates
        ├── base.html
        └── home_view.html
    ```

1. in TEMPLATES in django_learning/settings.py add templates directory as follow
    ```
        TEMPLATES = [
        {
            'DIRS': [
                BASE_DIR / 'templates', #<------------- add here (make sure to add ``BASE_DIR /`` to every directory you want to add)
            ],  
        },
        ]
    ```


1. in django_learning/views.py add following imports
    ```
    from articles.models import Article
    from django.template.loader import render_to_string
    ```
1. get the stored object by (only if you have saved a model)

    ```article = Article.objects.get(id=1)```

1. store model properties into a map as follow
    ```
    context = {"title": article.title,
               "content": article.content,
               "id": article.id, }
    ```

1. pass dictionary to html page by
    ```HTML_STRING = render_to_string("home_view.html", context=context)```

1. return response by
    ```return HttpResponse(HTML_STRING)```

# Sending variables to html
1. in templates/home_view.html add all the variable that you want to receive from django_learning/views.py in double curly brackets ({{}}), make sure the variable names are same as the name you are passing through context directory

home_view.html will look like
```
<h1>article title = {{title}}<br />article content = {{content}}<br />id = {{id}}</h1>
```
1. refresh the web page and you will get the values that you stored in the model

# extending a template
> in templates/home_view.html
1. add ``{% extends "base.html" %}`` at the top, base.html will be the file, where you want to display content of home_view.html
1. add ```{% block heading %}``` to the beginning of of content you want to display in base.html
    > you can put any name instead of ```heading```
1. add {% endblock heading %} to the end of of content you want to display in base.html
1. home_view.html should look like 
    ```
    <!-- Content here will be replaced in view  -->
    {% extends "base.html" %}
    {% block heading %}
    <!-- values to be substituted must be enclosed in double curly brackets ("{{variable}}")  -->
    <h1>article title = {{title}}<br />article content = {{content}}<br />id = {{id}}</h1>
    {% endblock heading %}
    ```
> in templates/base.html
1. add following code to the place where you want to display content of heading block
    ```
    {% block heading %}
    <p>any thing here will we replaced</p>
    {% endblock heading %}
    ```
    > any thing between ```{% block heading %}``` and ```{% endblock heading %}``` will be replaced by the content provided by home_view.html

    base.html will look like
    ```
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Home View</title>
    </head>
    <body>
        {% block heading %}
        <p>any thing here will we replaced</p>
        {% endblock heading %}
        
    </body>
    </html>

    ```

1. refresh the web page and see the changes

# Passing List to html
1. pass the list to html page using context
```
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

```

1. in html page we can use for loops
    - start for loop as:
    ```
    
    {% for x in my_list %}
     
    ```
    - access variable using the name you do in python like ```{{x}}```
    complete code
    ```
    <ul>
    {% for x in my_list %}
    <li>{{x}}</li>
    {% endfor %}
    </ul>

    <h1>Query Set</h1>
    <ul>
    {% for x in qs %}
    {% if x.title %}
    <li> <a href="/articles/{{x.id}}">{{x.title}}</a> </li>
    {% endif %}
    {%endfor%}
    </ul>
    ```

> if you want to use any control flow statement, make sure to close it like 

```
{% for x in my_list %} # Beginning
{% endfor %} # end
```

# Dynamic Routing
1. in ```django_learning/urls.py``` add dynamic route as
    ```
    path('articles/<int:id>', article_detail_view),
    ```

2. in ```articles/views.py``` add your logic
    ```
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

    ```

3. refresh the page and hit the url

# Creating an admin 
run 
```
python manage.py createsuperuser
```

enter id and password
hit 
```
http://127.0.0.1:8000/admin
```
enter id and password to login

# Adding models to admin panel

1. open ```articles/admin.py```
1. import your model
1. make a class that extends ```admin.ModelAdmin```
1. in class set following properties
    1. ```list_display = ['id', 'title']```
    1. ```search_fields = ['title']```
    > these two lines will do following

    list_display will add fields in table in admin panel
    |id|title|
    |:--|:--|
    |1|title 1|
    |2|title 2|

    > search_fields will add a search bar, and we will be able to search object by the attributes we passed in list
   