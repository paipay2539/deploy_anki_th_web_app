cd %CD%\project_env
cmd /k "Scripts\activate && cd .. && cd /d anki_th_web_app_project & python manage.py runserver 0.0.0.0:8000 && cd .."
