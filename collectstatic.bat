cd %CD%\project_env
cmd /k "Scripts\activate && cd .. && cd /d python manage.py collectstatic"
