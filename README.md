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
> change version to latest version, I am learning from old tutorials/books that is why I am using an old version

# Creating requirements.txt
this file is used to store name of packages that we have installed to make the project, it also store dependencies that automatically gets installed while we install a package to make requirements.txt run
```
pip freeze > requirements.txt
```

# Installing packages from requirements.txt
run 
```bash
pip install -r requirements.txt
```

# Creating django project 
```bash
django-admin startproject <your project name> .
```
>  ( . ) at the end of the command indicates current directory, you may replace it the directory where you want to create django project

if done correctly following will be the directory structure
> for future reference name of my project is ```django_learning```

```bash
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
```bash
python manage.py reserver
```

> it will give following output 

```bash
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
```bash
You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
```

run 
```bash
python manage.py migrate
```

# Changing home page (HelloWorld)
1. inside your project folder (django_learning) in my case, create views.py

1. inside views .py add following 
    ```python
    from django.http import HttpResponse
    def home_view(request):
        return HttpResponse("<h1>Hello World</h1>")
    ```
1. inside django_learning/urls.py
    - import home_view by ```from .views import home_view```
    - in urlpatterns list add ```path('',view=home_view)```
    - it would look like
        ```python
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
    ```python
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
    ```python
    from django.db import models
    class Article(models.Model):
        title = models.TextField()
        content = models.TextField()
    ```

1. run 
    ```bash
    python manage.py makemigrations
    python manage.py migrate 
    ```

# Saving Models to storage for feature use
1. run ```python manage.py shell```, it will open django python shell
1. in shell run
    ```python
    from articles.models import Article
    obj = Article.objects.create(title="title", content="content")
    obj.save()
    obj.id
    ```
    in the end program will return object id (usually it will be 1)

1. in feature we will do it programmatically, this is up until then

# Creating web template
1. create a folder called template in root of your project
1. create base.html
1. create home_view.html <br/>
    folder will look like
    ```bash
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
    ```python
    TEMPLATES = [
    {
        'DIRS': [
            BASE_DIR / 'templates', #<------------- add here (make sure to add ``BASE_DIR /`` to every directory you want to add)
        ],  
    },
    ]
    ```


1. in django_learning/views.py add following imports
    ```python
    from articles.models import Article
    from django.template.loader import render_to_string
    ```
1. get the stored object by (only if you have saved a model)

    ```python
    article = Article.objects.get(id=1)
    ```

1. store model properties into a map as follow
    ```python
    context = {"title": article.title,
               "content": article.content,
               "id": article.id, }
    ```

1. pass dictionary to html page by
    ```python
    HTML_STRING = render_to_string("home_view.html", context=context)
    ```

1. return response by
    ```python
    return HttpResponse(HTML_STRING)
    ```

# Sending variables to html
1. in templates/home_view.html add all the variable that you want to receive from django_learning/views.py in double curly brackets ({{}}), make sure the variable names are same as the name you are passing through context directory

home_view.html will look like
```html
<h1>article title = {{title}}<br />article content = {{content}}<br />id = {{id}}</h1>
```
1. refresh the web page and you will get the values that you stored in the model

# Extending a template
> in templates/home_view.html
1. add ``{% extends "base.html" %}`` at the top, base.html will be the file, where you want to display content of home_view.html
1. add ```{% block heading %}``` to the beginning of of content you want to display in base.html
    > you can put any name instead of ```heading```
1. add {% endblock heading %} to the end of of content you want to display in base.html
1. home_view.html should look like 
    ```html
    <!-- Content here will be replaced in view  -->
    {% extends "base.html" %}
    {% block heading %}
    <!-- values to be substituted must be enclosed in double curly brackets ("{{variable}}")  -->
    <h1>article title = {{title}}<br />article content = {{content}}<br />id = {{id}}</h1>
    {% endblock heading %}
    ```

1. **in templates/base.html** add following code to the place where you want to display content of heading block
    ```html
    {% block heading %}
    <p>any thing here will we replaced</p>
    {% endblock heading %}
    ```
    > any thing between ```{% block heading %}``` and ```{% endblock heading %}``` will be replaced by the content provided by home_view.html

    base.html will look like
    ```html
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
    ```python
    from django.template.loader import render_to_string
    from articles.models import Article
    from django.http import HttpResponse


    def home_view(request):
        article = Article.objects.get(id=1)
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
    ```html
    
    {% for x in my_list %}
     
    ```
    - access variable using the name you do in python like ```{{x}}```
    complete code
    ```html
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
    ```python
    path('articles/<int:id>', article_detail_view),
    ```

1. in ```articles/views.py``` add your logic
    ```python
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

1. refresh the page and hit the url

# Creating an admin 
run 
```bash
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

    - ```list_display = ['id', 'title']``` list_display will added fields in table in admin panel as follow

    |id|title|
    |:--|:--|
    |1|title 1|
    |2|title 2|

    - ```search_fields = ['title']```  will add a search bar, and we will be able to search object by the attributes we passed in list

**Final Code** ```articles/admin.py``` :

```python
from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']


admin.site.register(Article, ArticleAdmin)
```

# Simple Get request
1. create ```templates/articles/search.html```
    ```html
    {% extends "base.html" %}
    {% block base %}

    {% if article_obj != None %}
    Passed Object Id = {{article_obj.id}} <br />
    Passed Object Title = {{article_obj.title}} <br />
    Passed Object Content = {{article_obj.content}} <br />
    {% endif %}
    {% endblock base %}
    ```
1. add search box in ```templates/base.html```
    ```html
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Home View</title>
    </head>

    <body>
        <h1>Search Box</h1>
        <form action="/articles/">
            <input type="text" name="q">
            <input type="submit">
        </form>
        <br/>
        {% block base %}
        <p>any thing here will we replaced</p>
        {% endblock base %}

    </body>

    </html>
    ```

1. create ```article_search_view``` in ```articles/views.py```
    ```python
    def article_search_view(request: HttpRequest):
        query = None
        article_obj = None

        try:
            query = request.GET['q']
            query = int(query)
            article_obj = Article.objects.get(id=query)
            context['article_obj'] = article_obj

        except:
            query = None
            article_obj = None
            
        context = {
            'article_obj': article_obj
        }
        return render(request=request, context=context, template_name='articles/search.html')
    ```
    > we can get request parameters by ```query = request.GET['<Parameter Name>']```

    > To minimize code, we can use render from django shortcuts, and I'll use it from current codes, Usage

    ```python
    from django.shortcuts import render
    from .models import Article
    from django.http import HttpRequest

    def article_search_view(request: HttpRequest):
        query = None
        article_obj = None

        try:
            query = request.GET['q']
            query = int(query)
            article_obj = Article.objects.get(id=query)
            context['article_obj'] = article_obj

        except:
            query = None
            article_obj = None

        context = {
            'article_obj': article_obj
        }
        return render(request=request, context=context, template_name='articles/search.html') #<-------------- using render instead of render_to_string
    ```

1. add path in ```django_learning/urls.py```
    ```python
    from django.contrib import admin
    from django.urls import path
    from .views import *
    from articles import views

    urlpatterns = [
        path('', home_view),
        path('admin/', admin.site.urls),
        path('articles/', views.article_search_view),
        path('articles/create', views.article_create_view),
        path('articles/<int:id>', views.article_detail_view),

    ]
    ```

# Simple Post Request
1. in ```articles/views.py``` add create_view
    ```python
    def article_create_view(request: HttpRequest):
        context = {}

        if (request.method == 'POST'):
            title = request.POST.get('title')
            content = request.POST.get('content')
            article_obj = Article.objects.create(title=title, content=content)
            context['article_obj'], context['created'] = article_obj,  True

        return render(request=request, context=context, template_name='articles/create.html')
    ```

    > ```if (request.method == 'POST'):``` to perform actions only on post request

1. register url in ```django_learning/urls.py```
    ```python
    urlpatterns = [
        path('', home_view),
        path('admin/', admin.site.urls),
        path('articles/', views.article_search_view),
        path('articles/create/', views.article_create_view),
        path('articles/<int:id>', views.article_detail_view),

    ]
    ```
    > always remember just like express in java-script, order of url does effect the program

1. create ```templates/articles/create.html``` 
    ```HTML
    {% extends "base.html" %}
    {% block base %}
    <h1>Create.html</h1>

    {% if not created %}

    <div style="margin-top: 30px;">
        <form action="." method="post">
            {% csrf_token %}
            <div style="margin-top: 30px;">
                <input type="text" name="title" placeholder="Title" required />
            </div>
            <div style="margin-top: 10px;">
                <textarea name="content" placeholder="Content" required></textarea>
            </div>
            <button type="submit">Create Article</button>
        </form>
    </div>

    {% else %}
    Passed Object Id = {{article_obj.id}} <br />
    Passed Object Title = {{article_obj.title}} <br />
    Passed Object Content = {{article_obj.content}} <br />
    {% endif %}

    {% endblock base %}
    ```

# Creating Login Page
To deal with logging or logging out, I have created another module called accounts
1. create module name accounts
    ```bash
    python manage.py startapp accounts
    ```

1. Register it in ```django_learning/settings.py```
    ```python
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'articles',
        'accounts', #<------------ added accounts
    ]
    ```

1. create view in ```accounts/views.py``` **(login_view)**
    ```python
    from django.contrib.auth import login, authenticate
    from django.shortcuts import render, redirect
    from django.http import HttpRequest


    def login_view(request: HttpRequest):

        # checking if request is a POST request
        if request.method == 'POST':
            # getting username and passwords
            username = request.POST.get('username')
            password = request.POST.get('password')

            # authenticate user
            user = authenticate(
                request=request, username=username, password=password,)

            # check if user is invalid, if invalid re-render page with error
            if user is None:
                return render(request=request, template_name='account/login.html', context={"error": "Invalid Username Or Password"})

            # if user is valid log the user in
            login(user=user,request=request)

            # re-direct user to whatever page you want
            return redirect("/admin")

        # for GET requests
        return render(request=request, template_name='account/login.html', context={})

    ```

1. create ```templates/account/login.html```
    ```html
    {% extends "base.html" %}

    {% block base %}

    <div style="margin-top: 30px;">
        <!-- check if there is error, if error show message -->
        {% if error %}
        <p style="color: red;"> {{error}} </p>
        {% endif %}
        <!-- Login Form, as action is not specified it will target current url -->
        <form method="post">
            {% csrf_token %}
            <div>
                <label for="username">User Name</label>
                <input type="text" name="username" placeholder="User Name" />
            </div>
            <div style="margin-top: 10px;">
                <label for="password">Password</label>
                <input type="password" name="password" placeholder="Password" />
            </div>
            <button type="submit">Login</button>
        </form>
    </div>

    {% endblock base %}
    ```

1. add paths in ```django_learning/urls.py```
    ```python
    from django.contrib import admin
    from django.urls import path
    from .views import *
    from articles import views as article
    from accounts import views as accounts

    urlpatterns = [
        path('', home_view),
        path('admin/', admin.site.urls),

        # For Articles
        path('articles/', article.article_search_view),
        path('articles/create/', article.article_create_view),
        path('articles/<int:id>', article.article_detail_view),

        # For accounts
        path('login', accounts.login_view),

    ]

    ```
    > we can use ```request.user.is_authenticated``` to check if user is authenticated

# Creating Logout Page
as discussed above we can use ```request.user.is_authenticated``` in python program to check if user is authenticated or not, but what if want to check the exact in html template?

django is here to save our day in ```django_learning/settings.py``` check ```context_processors```

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [ # <--- these are the libraries can be accessed in any html template as django already imports these libraries to any html template we render
                'django.template.context_processors.debug',
                'django.template.context_processors.request', 
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

So, django by default imports ```django.template.context_processors request and django.contrib.auth.context_processors.auth``` 

it means we can use ```request.user.is_authenticated``` in html pages as well, without any need of passing it through context

1. we can edit our ```templates/account/login.html``` as 

    ```html
    {% extends "base.html" %}

    {% block base %}

    <div style="margin-top: 30px;">
        <!-- if user is not authenticated, show login form -->
        {% if not request.user.is_authenticated %}
        {% if error %}
        <p style="color: red;"> {{error}} </p>
        {% endif %}
        <form method="post">
            {% csrf_token %}
            <div>
                <label for="username">User Name</label>
                <input type="text" name="username" placeholder="User Name" />
            </div>
            <div style="margin-top: 10px;">
                <label for="password">Password</label>
                <input type="password" name="password" placeholder="Password" />
            </div>
            <button type="submit">Login</button>
        </form>
        {% else %}
        <!-- else show logout message -->
        <p>Your're already logged in, would you like to <a href="/logout/">logout</a></p>
        {% endif %}
    </div>

    {% endblock base %}
    ```
    >login and re-visit ```http://127.0.0.1:8000/login``` to confirm

1. create ```templates/account/logout.html``` 
    ```html
    {% extends "base.html" %}

    {% block base %}

    <div style="margin-top: 30px;">
        <!-- if user if logged in, show logout confirmation for -->
        {% if request.user.is_authenticated %}
        <form method="post">
            {% csrf_token %}
            <p>are you sure you want to logout</p>
            <button type="submit">Yes, Logout</button>
        </form>
        {% else %}
        <!-- else show login link -->
        <p>Your're not logged in, would you like to <a href="/login/">Login</a></p>
        {% endif %}
    </div>

    {% endblock base %}
    ```

1. in ```accounts/views.py``` add ```logout_view```
    ```python
    from django.contrib.auth import login, authenticate, logout #<-- add logout import

    def logout_view(request: HttpRequest):
        if (request.method == 'POST'):
            logout(request=request)
            return redirect('/login/')

        return render(request=request, template_name='account/logout.html')
    ```

1. register url in ```django_learning/urls.py```
    ```python
    from django.contrib import admin
    from django.urls import path
    from .views import home_view
    from articles import views as article
    from accounts import views as accounts

    urlpatterns = [
        path('', home_view),
        path('admin/', admin.site.urls),

        # For Articles
        path('articles/', article.article_search_view),
        path('articles/create/', article.article_create_view),
        path('articles/<int:id>', article.article_detail_view),

        # For accounts
        path('login/', accounts.login_view),
        path('logout/', accounts.logout_view),

    ]

    ```

# Making login required mandatory for create article
1. import login_required decorator

    ```python
    from django.contrib.auth.decorators import login_required
    ```

1. add ```@login_required``` decorator to the ```article_create_view```

    ```python
    @login_required
    def article_create_view(request: HttpRequest):
    ```

1. add ```LOGIN_URL``` variable and assign your login path in ```django_learning/settings.py```

    ```python
    LOGIN_URL = '/login
    ```

1. logout and then hit ```http://127.0.0.1:8000/articles/create/``` you will be redirected to login page with next argument, we will handle the next argument later.

# Using django forms basics
we want to create django form for article creation, so we make ```articles/forms.py```

1. in ```articles/forms.py``` make a class extending ```from django import forms.Form```

    ```python
    from django import forms
    class ArticleForm(forms.Form):
    ```

1. declare fields in ```ArticleForm``` class as per requirement
    ```python
    class ArticleForm(forms.Form):
        title = forms.CharField()
        content = forms.CharField()
    ```

1. in ```articles/views.py```
    - import ```ArticleForm``` class
        ```python
        from .forms import ArticleForm
        ```

    - in ```article_create_view``` initialize ```ArticleForm()``` instance and pass it to ```create.html``` using context
        ```python
        @login_required
        def article_create_view(request: HttpRequest):
            form = ArticleForm(request.POST or None) # initializing ArticleFrom class instance
            context = {'form': form}

            if (request.method == 'POST'):
                title = request.POST.get('title')
                content = request.POST.get('content')
                article_obj = Article.objects.create(title=title, content=content)
                context['article_obj'], context['created'] = article_obj,  True

            return render(request=request, context=context, template_name='articles/create.html')
        ```

1. in ```templates/articles/create.html``` delete fields which we previously made and use form we are passing through context

    ```html
    {% extends "base.html" %}
    {% block base %}
    <h1>Create.html</h1>

    {% if not created %}
    <div style="margin-top: 30px;">
        <form action="." method="post">
            {% csrf_token %}
            <!-- {{form.as_p}} is going to render our form that we passed through context in paragraph format -->
            {{form.as_p}}
            <button type="submit">Create Article</button>
        </form>
    </div>

    {% else %}
    Your article was created <br/>
    <a href="/articles/{{article_obj.id}}"> {{article_obj.title}} </a>
    {% endif %}

    {% endblock base %}
    ```

    now hit ```http://127.0.0.1:8000/articles/create/``` and see the changes

1. Adding validation for creating article
    - add validators in ```articles/forms.py```

        ```python
        from typing import Any
        from django import forms


        class ArticleForm(forms.Form):
            title = forms.CharField()
            content = forms.CharField()
            """
            Validation or clean methods, to validate forms or validate the forms we have two methods
            1. field specific validation
            2. whole form validation
            """

            # field validation, to do field validation create a method called clean_<your field name>(self)

            def clean_title(self) -> str:
                # Dictionary containing the field i.e it will only be containing title only ({'title': 'value'})
                cleaned_data = dict(self.cleaned_data)
                title = cleaned_data.get('title')
                # add validation logic here
                if 'form' in title.lower():
                    raise forms.ValidationError(
                        'substring form can not be present in title')

                return title

            # whole form validation declare method called clean(self)
            # remember you can not have field validation methods if you have whole form validation method.

            def clean(self) -> dict[str, Any]:
                form_str = 'form'
                # Dictionary containing all of the fields ({'title': 'value','content':'value'})
                cleaned_data = dict(self.cleaned_data)
                title = str(cleaned_data.get('title'))
                content = str(cleaned_data.get('content'))
                # here can also throw both type of error field error as well as non-field error
                if form_str in content.lower() and form_str in title.lower():
                    raise forms.ValidationError(
                        'substring form present in both, content and title')
                
                if form_str in title.lower():
                    self.add_error(field='title',error='title contains substring form')

                if form_str in content.lower():
                    self.add_error(field='content',error='content contains substring form')

                return cleaned_data
        ```
    
    - check for validation in ```article_create_view```
        ```python
        @login_required
        def article_create_view(request: HttpRequest):
            form = ArticleForm(request.POST or None)
            context = {'form': form}

            if (request.method == 'POST'):
                # Checking if submitted data is validated
                if form.is_valid():
                    # getting cleaned from form
                    title = form.cleaned_data.get('title')
                    content = form.cleaned_data.get('content')

                    article_obj = Article.objects.create(title=title, content=content)
                    context['article_obj'], context['created'] = article_obj,  True

            return render(request=request, context=context, template_name='articles/create.html')    
        ```
        now hit ```http://127.0.0.1:8000/articles/create/``` and try to create article, in code above we have added validation that we can not have string ```form``` in title or content

# Undocumented Changes
> I have done Some Un-Documented Changes, Check Git log / Git History to see changes

# Model Forms
We can use forms based on our Models, We are going to use our previously build Article model


1. In ```articles/forms.py``` create class ```ArticleForm``` (remove previously created class) that extends ```forms.ModelForm```

    ```python
    class ArticleForm(forms.ModelForm):
    ```

1. declare class meta in ```ArticleForm``` class
    - assign model as Article 
    - declare fields array containing name of fields that are declared in Articles Model
    ```python
    class ArticleForm(forms.ModelForm):
        class Meta:
            model = Article
            fields = ['title', 'content']
    ```

1. define clean or clean_&lt;field name&gt;() method

    Whole Code
    ```python
    from typing import Any
    from django import forms
    from .models import Article


    class ArticleForm(forms.ModelForm):
        class Meta:
            model = Article
            fields = ['title', 'content']

        def clean(self) -> dict[str, Any]:
            data = dict(self.cleaned_data)
            title = data.get('title')
            # Method to check if data base already contains submitted title
            qs = Article.objects.filter(title__icontains=title)
            if qs.exists():
                self.add_error('title', f"{title} already in used")
            return super().clean()

    ```

1. in ```articles/views.py``` modify ```article_create_view```
    ```python
    @login_required
    def article_create_view(request: HttpRequest):
        form = ArticleForm(request.POST or None)
        context = {'form': form}

        if (request.method == 'POST'):
            if form.is_valid():
                article_obj = form.save()
                context['article_obj'], context['created'] = article_obj,  True

        return render(request=request, context=context, template_name='articles/create.html')
    ```

# Adding Links in Home view
1. pass list of all urls in home_view in ```django_learning/views.py```
    ```python
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
        ] # list of all urls with name
        query_set = Article.objects.all()
        context['my_list'], context['qs'], context["article_obj"], context['url_list'] = my_list, query_set, article, url_list

        HTML_STRING = render_to_string("home_view.html", context=context)
        return HttpResponse(HTML_STRING)

    ```

1. parse in ```templates/home_view.html```
    ```html
    <h2>All Urls Available</h2>
    {% for x in url_list %}
        <a href="{{x.url}}"> {{x.name}} </a> <br>
    {%endfor%}
    ```

1. whole file 
    ```html
    <!-- Content here will be replaced in view  -->
    {% extends "base.html" %}
    {% block base %}
    <h1>Home_View.html</h1>
    <h2>Passed List For Parsing</h2>
    <ul>
        {% for x in my_list %}
        <li>{{x}}</li>
        {% endfor %}
    </ul>

    <!-- values to be substituted must be enclosed in double curly brackets ("{{variable}}")  -->
    {% if article_obj %}
    <h2>
        Article 1 Details
    </h2>
    <h3>
        Title = {{article_obj.title}}<br />
        Content = {{article_obj.content}}<br />
        Id = {{article_obj.id}} <br />
    </h3>

    {% endif %}

    <h2>All Urls Available</h2>
    {% for x in url_list %}
        <a href="{{x.url}}"> {{x.name}} </a> <br>
    {%endfor%}

    <h2>All Data in Database</h2>
    <ul>
        {% for x in qs %}
        {% if x.title %}
        <li> <a href="/articles/{{x.id}}">{{x.title}}</a> </li>
        {% endif %}
        {%endfor%}
    </ul>
    {% endblock base %}
    ```

# Built in sign up from
1. in ```accounts/views.py``` create ```signup_view```
    ```python
    # Add following import
    from django.contrib.auth.forms import UserCreationForm # Django's built in User creation Form

    def signup_view(request : HttpRequest):
        context = {}
        signup_form = UserCreationForm(request.POST or None)
        if signup_form.is_valid():
            signup_form.save()
            return redirect("/login")
        
        context['form'] = signup_form
        return render(request= request,context=context,template_name='account/signup.html')
    ```

1. create ```templates/account/signup.html```
    ```html
    {% extends "base.html" %}

    {% block base %}
    <h1>Signup.html</h1>

    <div style="margin-top: 30px;">
        {% if not request.user.is_authenticated %}
        {% if error %}
        <p style="color: red;"> {{error}} </p>
        {% endif %}
        <form method="post">
            {% csrf_token %}
            {{form.as_p}}
            <button type="submit">Login</button>
        </form>
        {% else %}
        <p>Your're already logged in, Can not create a user would you like to <a href="/logout/">logout</a></p>
        {% endif %}
    </div>

    {% endblock base %}
    ```

1. add path in ```django_learning/urls.py```
    ```python
    urlpatterns = [
        path('', home_view),
        path('admin/', admin.site.urls),

        # For Articles
        path('articles/', article.article_search_view),
        path('articles/create/', article.article_create_view),
        path('articles/<int:id>', article.article_detail_view),

        # For accounts
        path('login/', accounts.login_view),
        path('logout/', accounts.logout_view),
        path('signup/', accounts.signup_view),

    ]
    ```

1. in ```django_learning/views.py``` add url in url_list
    ```python
    url_list = [
            {"name": "admin panel", "url": "/admin/"},
            {"name": "Create Article", "url": "/articles/create/"},
            {"name": "Article Details", "url": "/articles/1"},
            {"name": "Login", "url": "/login/"},
            {"name": "Logout", "url": "/logout/"},
            {"name": "Signup", "url": "/signup/"}, # signup url
        ]
    ```

# Built in login form 
Here I am going to replace custom made login form with built in django login form 

1. in ```accounts/views.py``` import user authentication form 
    ```python
    from django.contrib.auth.forms import AuthenticationForm
    ```

1. modify the ```login_view``` as 
    ```python
    def login_view(request: HttpRequest):
        form = None
        context = {}
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(user=user, request=request)
                return redirect("/")

        else:
            form = AuthenticationForm(request=request)
        
        context['form'] = form

        return render(request=request, template_name='account/login.html', context=context)
    ```

1. modify ```templates/account/login.html``` to use form passed through context
    ```html
    {% extends "base.html" %}

    {% block base %}
    <h1>Login.html</h1>

    <div style="margin-top: 30px;">
        {% if not request.user.is_authenticated %}
        <form method="post">
            {% csrf_token %}
            {{form.as_p}}
            <button type="submit">Login</button>
        </form>
        {% else %}
        <p>Your're already logged in, would you like to <a href="/logout/">logout</a></p>
        {% endif %}
    </div>

    {% endblock base %}
    ```

> visit http://localhost:8000/login/ to view changes

# Preparing For Production server

> I tried using [django-dotenv](https://pypi.org/project/django-dotenv/) but it does not work well with production server so I am not using it , instead I am Using gunicorn for setting environment variables as we are already going to use gunicorn in production as python server, I might use [django-dotenv](https://pypi.org/project/django-dotenv/) for unit testing as we can't use gunicorn for that


1. Installing gunicorn
    ```bash
    pip install gunicorn
    ```

    > following steps in ```django_learning/settings.py```

1. Using environment variables to set properties in settings.py
    ```python
    # add this import
    import os

    # Modify these
    DEBUG = os.environ.get('DEBUG', '0') == '1'

    # replace Default Key with key that is already there
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Default key')
    ```

1. adding allowed hosts: <br/>
    allowed hosts tells django on what ip should it serve, if you are using custom domain you may put it here, for local host it will be
    ```python
    # Modify this
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
    ```


1. add STATIC_ROOT <br/>
    static_root tells the location of the folder that contains all the css and other static files
    ```python
    STATIC_ROOT = BASE_DIR / 'static'
    ```

1. optional: change logs timezone
    ```python
    # modify it to change timezone in logs
    TIME_ZONE = 'Asia/Kolkata'
    ```


1. collect all static files 
    ```bash
    python manage.py collectstatic  
    ```
    it will generate static folder with admin static files

    
1. configure gunicorn options and add environment variables
    > following steps in ```gunicorn.conf.py``` (make the file if does not exists)
    ```python
    # number of worker nodes depending on your system
    workers = 8

    # your linux user name
    user = 'gtirkha'
    # your linux user name
    group = 'gtirkha'

    # location of logs
    errorlog = 'error.log'
    accesslog = 'access.log'

    # your ip and port, ,on which you want django to serve
    bind = '127.0.0.1:8000'

    # your directory of django project
    chdir = '/home/gtirkha/Documents/django_learning'

    # set Environment variables here
    # should be in "key=value" form, separated with comma (,)
    # all the variable will be of string data type
    raw_env = [
        "SECRET_KEY=*)this_is_my_key(*",
        "DEBUG=0",
    ]

    ```

1. in settings.py find value of ```WSGI_APPLICATION```
    ```python
    WSGI_APPLICATION = 'django_learning.wsgi.application'
    ```    
    run 
    ```bash
    gunicorn django_learning.wsgi:application  
    ```
    > don't forget to replace ( . ) before application with colon ( : )

1. visit ```localhost:8000``` to view page ( as we set in gunicorn.conf.py )

    > if you visit ```http://localhost:8000/admin/``` if debug mode is set to false the page will not have any css, as static files are not being served, we will learn how to do it in deployment part using nginx but if you want you can use [whitenoise](https://pypi.org/project/whitenoise/)
    
    > following steps are optional as we are going to use nginx to serve static files, how ever if you don't want to do it using nginx you may follow following

1. install whitenoise
    ```bash
    pip install whitenoise  
    ```

1. add whitenoise middleware in ```django_learning/settings.py```
    ```python
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        "whitenoise.middleware.WhiteNoiseMiddleware", #<-------Whitenoise middleware
    ]
    ```

1. re-run gunicorn and now check ```http://localhost:8000/admin``` we will now have css there

# Writing unit tests
> gunicorn can't be used for test cases, so for configuring environment variables we are using [django-dotenv](https://pypi.org/project/django-dotenv/)

1. Install ```django-dotenv```
    ```bash
    pip install django-dotenv
    ```

1. in ```manage.py```
    ```python
    # Import dotenv
    import dotenv

    def main():
        """Run administrative tasks."""
        # add this line
        dotenv.read_dotenv()

    ```

1. create ```django_learning/tests.py```
    - import test case ```from django.test import TestCase```
    - make a class that extends ```TestCase```
    - define functions in class with name starting with ```test_``` and ```self``` as parameter
    - use self.fail() to fail the test
    > we can also use self.assert &lt;Condition&gt; methods to assert if test fails

    This code tests the strength of ```SECRET_KEY``` environment variable
    ```python
    import os
    from django.test import TestCase
    from django.contrib.auth.password_validation import validate_password


    class MyTestCases(TestCase):
        def test_key(self):
            KEY = os.environ.get('SECRET_KEY')
            self.assertAlmostEqual
            try:
                validate_password(KEY)
            except Exception as e:
                message = e.messages
                self.fail(msg=message)
    ```
1. create .env file and define environment variable
    ```text
    SECRET_KEY=*)this_is_my_key(*
    DEBUG=0
    ```

1. run test cases
    ```bash
    python manage.py test
    ```
> we can make test.py for every model / app but I might not do that as my current aim is learning

# Editing Models
I have done some changes in article models as follow
1. ```articles/models.py```

    ```python
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
    ```

1. ```articles/forms.py```

    ```python
    from typing import Any
    from django import forms
    from .models import Article


    class ArticleForm(forms.ModelForm):
        class Meta:
            model = Article
            # added publish_date
            fields = ['title', 'content', 'publish_date']

        def clean(self) -> dict[str, Any]:
            data = dict(self.cleaned_data)
            title = data.get('title')
            qs = Article.objects.filter(title__icontains=title)
            if qs.exists():
                self.add_error('title', f"{title} already in used")
            return super().clean()
    ```

1. ```articles/admin.py```

    ```python
    from django.contrib import admin
    from .models import Article


    # added updated_on and created_on
    class ArticleAdmin(admin.ModelAdmin):
        list_display = ['id', 'title', 'updated_on', 'created_on']
        search_fields = ['title']


    admin.site.register(Article, ArticleAdmin)
    ```

1. run in terminal
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
    > if asked to provide default value for time fields, press 1 to provide default value and the enter ```timezone.now``` and hit enter

1. run server and view changes

# Adding a slug field in article
1. add slug field in ```articles/models.py```

    ```python
    slug = models.SlugField(blank=True, null=True)
    ```

1. override save method to add value to slug fields
    ```python
    def save(self, *args, **kwargs) -> None:
        if self.slug is None:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)
    ```

1. run in terminal
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

1. run server and visit ```http://localhost:8000/admin/articles/article/add/``` to view changes, if you don't add any value to slug field the slugged title will be saved

# Generating Unique slugs and using pre_save and post_save signals

> I have removed save method in ```articles/models.py```

> **pre_save** and **post save** :- pre_save is triggered before save method of model and post save is triggered after save method of model.

> post_save signal provides created bool which can be used to determine if the model was newly created

> I want to add slugs in ```list_display``` and ```search_fields``` so that I can view and search slugs in admin panel table

1. in ```articles/admin.py```

    ```python
    from django.contrib import admin
    from .models import Article


    class ArticleAdmin(admin.ModelAdmin):
        # add slugs in these 2 lists
        list_display = ['id', 'slug', 'title', 'updated_on', 'created_on']
        search_fields = ['title', 'slug']


    admin.site.register(Article, ArticleAdmin)
    ```

1. ```articles/models.py``` 
    - import pre_save and post_save
    
        ```python
        from django.db.models.signals import pre_save, post_save
        ```
    
    - define methods to be performed on pre_save and post_save
    - connect pres_ave and post_save methods
        ```python
        pre_save.connect(receiver=your_method_name, sender=your_model_name)
        post_save.connect(receiver=your_method_name, sender=your_model_name)
        ```    

    ```python
    from collections.abc import Iterable
    from django.db import models
    from django.utils import timezone
    from django.utils.text import slugify
    from django.db.models.signals import pre_save, post_save


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

        # adding a slug field
        slug = models.SlugField(blank=True, null=True, unique=True)


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
    ```

# Using Slugs in stead of id 
1. in ```django_learning/urls.py```

    ```python
    path('articles/<slug:slug>', article.article_detail_view) # edit this path
    ```

1. in ```articles/views.py``` edit ```article_detail_view```
    ```python
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
    ```

1. in ```articles/views.py``` edit ```article_search_view```
    ```python
    def article_search_view(request: HttpRequest):
        query = None
        article_obj = None
        context = {}

        try:
            query = request.GET['q']
            article_obj = Article.objects.get(slug=query)

        except:
            query = None
            article_obj = None

        context['article_obj'] = article_obj
        return render(request=request, context=context, template_name='articles/search.html')
    ```

1. edit ```templates/home_view.html``` to use slugs
```html
<!-- Content here will be replaced in view  -->
{% extends "base.html" %}
{% block base %}
<h1>Home_View.html</h1>
<h2>Passed List For Parsing</h2>
<ul>
    {% for x in my_list %}
    <li>{{x}}</li>
    {% endfor %}
</ul>

<!-- values to be substituted must be enclosed in double curly brackets ("{{variable}}")  -->
{% if article_obj %}
<h2>
    Article 1 Details
</h2>
<h3>
    Title = {{article_obj.title}}<br />
    Content = {{article_obj.content}}<br />
    Id = {{article_obj.id}} <br />
</h3>

{% endif %}

<h2>All Urls Available</h2>
{% for x in url_list %}
    <a href="{{x.url}}"> {{x.name}} </a> <br>
{%endfor%}

<h2>All Data in Database</h2>
<ul>
    {% for x in qs %}
    {% if x.title %}
    <!-- Using Slugs instead of id -->
    <li> <a href="/articles/{{x.slug}}">{{x.title}}</a> </li> 
    {% endif %}
    {%endfor%}
</ul>
{% endblock base %}
```

# Using Links form model (making link getter in model class)
1. in ```articles/models.py``` Create a method which will return link to our object 

    ```python
    # adding url getter
        def url(self):
            return f'/articles/{self.slug}'
    ```

1. implement use in html files <br/>
```templates/articles/create.html```
    ```html
    <a href="{{article_obj.url}}"> {{article_obj.title}} </a>
    ```

    ```templates/home_view.html```
    ```html
    <li> <a href="{{x.url}}">{{x.title}}</a> </li>
    ```
