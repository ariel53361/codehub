release: python manage.py migrate
web: waitress-serve --host=0.0.0.0 --port=$PORT myproject.wsgi:application
