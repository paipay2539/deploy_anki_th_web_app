cd %CD%\anki_th_web_app_env
cmd /k "Scripts\activate && cd .. && cd /d anki_th_web_app_project & python manage.py collectstatic"
