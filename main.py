import argparse
import os
import re

parser = argparse.ArgumentParser(description="A test program")
parser.add_argument("createproject", help="creates_default_django_app")
parser.add_argument("projectname", help="project name here")
parser.add_argument("appname", help="app name here")


args = parser.parse_args()
if args.createproject == "createproject":
    project_name = args.projectname
    app_name = args.appname
    os.system(f"pip install django")
    os.system(f"django-admin startproject {project_name}")
    os.chdir(f"{project_name}")
    os.system(f"py manage.py startapp {app_name}")
    os.makedirs(os.path.join(app_name, 'templates'), exist_ok=True)
    os.makedirs(os.path.join(app_name, 'templates', app_name), exist_ok=True)
    urls_file_content = ("from django.urls import path\n"
                        f"from {app_name}.urls import *\n"
                        f"from {app_name}.models import *\n"
                        f"urlpatterns = [\n\n"
                        f"]")
    with open(os.path.join(app_name, 'urls.py'), 'w') as file:
        file.write(urls_file_content)

    urls_by_path = os.path.join(project_name, 'urls.py')

    with open(urls_by_path) as file:
        content = file.read()
        pattern = re.compile('import path', re.DOTALL)
        new = ('import path, include\n')
        content = pattern.sub(new, content)
        pattern = re.compile(r'\[\n', re.DOTALL)
        new = ''
        new += f"\tpath('', include('{app_name}')),\n"
        content = content.replace(']', new + ']')

    with open(urls_by_path, 'w') as file:
        file.write(content)

    setting_by_path = os.path.join(project_name, 'settings.py')

    with open(setting_by_path) as file:
        content = file.read(ч)
        pattern = re.compile("'django.contrib.staticfiles',\n", re.DOTALL)
        new_string = ("'django.contrib.staticfiles',\n"
                      f"\t'{app_name}',\n")
        content = pattern.sub(new_string, content)

    with open(setting_by_path, 'w') as file:
        file.write(content)



