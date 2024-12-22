import os

# Project and app names
project_name = "my_bot"
app_name = "bot"

# Define the file structure
file_structure = {
    project_name: {
        "__init__.py": "",
        "settings.py": """\
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-replace_this_with_a_secret_key'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_bot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_bot.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
""",
        "urls.py": """\
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bot.urls')),
]
""",
        "wsgi.py": """\
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_bot.settings')

application = get_wsgi_application()
""",
        "asgi.py": """\
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_bot.settings')

application = get_asgi_application()
""",
    },
    "manage.py": """\
#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_bot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""",
    app_name: {
        "__init__.py": "",
        "views.py": """\
from django.http import JsonResponse
from django.shortcuts import render
import google.generativeai as genai

# Configure generative AI
genai.configure(api_key="YOUR_ACTUAL_API_KEY")

def index(request):
    return render(request, 'index.html')

def generate_response(request):
    if request.method == "POST":
        import json
        body = json.loads(request.body)
        prompt = body.get('prompt', '')

        if not prompt:
            return JsonResponse({"error": "Prompt cannot be empty."}, status=400)

        try:
            response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
            return JsonResponse({"response": response.text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
""",
        "urls.py": """\
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate_response, name='generate'),
]
""",
        "templates": {
            "index.html": """\
<!DOCTYPE html>
<html>
<head>
    <title>AI Bot</title>
</head>
<body>
    <h1>Welcome to AI Bot</h1>
</body>
</html>
""",
        },
    },
}

# Recursive function to create the file structure
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):  # Create a folder
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:  # Create a file
            with open(path, "w") as f:
                f.write(content)

# Create the structure
base_dir = os.getcwd()
create_structure(base_dir, file_structure)

print("File structure created.")
