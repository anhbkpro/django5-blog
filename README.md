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
