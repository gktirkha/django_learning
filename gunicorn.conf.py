workers = 8
user = 'gtirkha'
group = 'gtirkha'
errorlog = 'error.log'
accesslog = 'access.log'
bind = '127.0.0.1:8000'
chdir = '/home/gtirkha/Documents/django_learning'

# set Environment variables here
raw_env = [
    "SECRET_KEY=*)this_is_my_key(*",
    "DEBUG=0",
]
