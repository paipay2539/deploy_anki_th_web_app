cd %CD%\project_env
cmd /k "Scripts\activate && cd .. && python manage.py runserver 0.0.0.0:8000 && cd .."
