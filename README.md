# django5-blog

## Creating a Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

## Installing Django
```bash
pip install django
```

## Creating a Django project
```bash
django-admin startproject mysite
```

## Applying initial database migrations
```bash
cd mysite
python manage.py migrate
```

## Running the development server
```bash
python manage.py runserver
```

*Note*: When you have to deal with multiple environments that require different configurations,
you can create a different settings file for each environment.
- You can run the Django development server on a custom host and port or tell Django to load a specific settings file, as follows:
```bash
python manage.py runserver 127.0.0.1:8001 --settings=mysite.settings
```

## Creating a Django app
```bash
cd mysite
python manage.py startapp blog
```
- Add the app to the `INSTALLED_APPS` list in the `mysite/settings.py` file.
- Create the database tables for the app by running the following command:
```bash
python manage.py migrate
```
- Add `Post` model to the `blog/models.py` file.
- Create the database tables for the `Post` model by running the following command:
```bash
python manage.py makemigrations blog

python manage.py sqlmigrate blog 0001

python manage.py migrate
Applying blog.0001_initial... OK
```
*Note*: If you edit the models.py file in order to add, remove, or change the fields of existing models, or if you add new models, you will have to create a new migration using the `makemigrations` command. Each migration allows Django to keep track of model changes. Then, you will have to apply the migration using the `migrate` command to keep the database in sync with your models.


## Creating a superuser
```bash
python manage.py createsuperuser
```

## Registering the Post model in the Django admin
- Add the following code to the `blog/admin.py` file:
```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

## Open the Python shell
```bash
python manage.py shell
```
