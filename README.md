# Reference
I am using [digitalocean guide](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04#creating-systemd-socket-and-service-files-for-gunicorn) to deploy the django project on server with some changes of my own like not migrating to Postgres (as it is a demo project) and not making gunicorn.socket file

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


# Deployment on Ubuntu Instance
we will deploy our django app on ubuntu instance like ec2 

1. install nginx

    ```bash
    sudo apt install nginx
    ```
1. clone project and make venv and install all the packages
    ```bash
    git clone <your project url>
    cd <project directory>
    python3 -m venv env
    source ./env/bin/activate
    pip install -r requirements.txt
    deactivate
    ```

1. change permission of your project to 777
    ```bash
    sudo chmod -R 777 <project dir>
    ```

1. add www-data to your user group
    ```bash
    sudo usermod -aG www-data <your_user_name> 
    ```
    > you can get your username by ```whoami``` command

1. remove white noise middleware if used (we are going to serve static files with the help of nginx)

1. change bind option to unix socket instead of IP in ```gunicorn.conf.py```
    ```python
    bind = 'unix:/run/gunicorn.sock'
    ```
    > you may choose any other name for ```gunicorn.sock``` but remember it, we will need it to setup nginx

1. remove ```raw_env``` from ```gunicorn.conf.py``` and remove ```dotenv.read_dotenv()``` from ```manage.py``` , we will use ```.env``` to load environment variables

1. create Systemd service to run gunicorn in background
    ```bash
    sudo nano /etc/systemd/system/gunicorn.service
    ```

    write the following in the nano editor
    ```
    [Unit]
    Description=gunicorn daemon
    After=network.target

    [Service]
    User=root
    Group=root
    WorkingDirectory=project_location
    ExecStart=<path to python venv environment>/bin/gunicorn django_learning.wsgi:application
    EnvironmentFile=/path/to/.env/file

    [Install]
    WantedBy=multi-user.target

    ```
1. press ctrl + O then enter to write changes and then ctrl + X to exit nano.

1. enable and start service
    ```
    sudo systemctl enable gunicorn.service 
    sudo systemctl start gunicorn.service 
    ```

1. check error logs for any errors

1. create nginx configuration
    ```bash
    cd /etc/nginx/sites-available 
    sudo nano django_deploy  
    ```

    and write following configuration
    ```text
    server  {
        listen  80;
        server_name <your-domain> or <your ip>;

        location = /favicon.ico { access_log off; log_not_found off; }

        location /static/   {
            root <your project location>
        }
        location / {
            include proxy_params;
            proxy_pass http:<your socket>;
            # example 
            # proxy_pass http://unix:/run/gunicorn.sock;
        }
    }
    ``` 

1. save file and exit nano
1. create soft link of configuration file and remove default site
    ```bash
    sudo ln -sf /etc/nginx/sites-available/django_deploy /etc/nginx/sites-enabled
    sudo rm -r /etc/nginx/sites-enabled/default
    ```
1. start nginx
    ```bash
    sudo systemctl enable nginx
    sudo systemctl start nginx
    ```

1. if server was already started then restart
    ```bash
    sudo nginx -s reload
    ```

1. add nginx to firewall allow list
    ```bash
    sudo ufw allow "Nginx Full"
    ```

1. now check that you have allowed http traffic to your instance, method varies according to provider

1. hit ip and, done. application deployed successfully

> ***To view nginx logs***
1. error logs

    ```bash
    cat /var/log/nginx/error.log
    ```
    or
    ```bash
    tail /var/log/nginx/error.log
    ```
1. access logs
    ```bash
    cat /var/log/nginx/error.log
    ```
    or 
    ```bash
    tail /var/log/nginx/error.log
    ```
    > tail will give last 10-15 logs, where cat will give all logs, you can also use vim or nano to view logs

1. if you make changes to project run following to restart server

    ```bash
    sudo systemctl start gunicorn.service
    sudo systemctl start nginx
    ```