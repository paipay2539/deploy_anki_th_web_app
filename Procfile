web: gunicorn anki_th_web_app_project.wsgi --log-file -
config: set DISABLE_COLLECTSTATIC=1
config: set DEBUG_COLLECTSTATIC=1
web: python manage.py collectstatic --no-input; gunicorn myapp.wsgi --log-file - --log-level debug