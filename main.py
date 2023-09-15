import argparse
import os
import re

'''

To run script simply drag main.py into created folder
Or paste code from the file
Then run into terminal:

'py main.py createproject {your project name here} {your app name here}'

'''

parser = argparse.ArgumentParser(description="A test program")
parser.add_argument("createproject", help="creates default django app")
parser.add_argument("projectname", help="project name here")
parser.add_argument("appname", help="app name here")


args = parser.parse_args()
if args.createproject == "createproject":
    project_name = args.projectname
    app_name = args.appname
    os.system(f"pip install django")
    print("Django is installed")
    os.system(f"django-admin startproject {project_name}")
    os.chdir(f"{project_name}")
    print("Project is created")
    os.system(f"py manage.py startapp {app_name}")
    os.makedirs(os.path.join(app_name, 'templates'), exist_ok=True)
    os.makedirs(os.path.join(app_name, 'templates', app_name), exist_ok=True)
    print("App is created")
    urls_file_content = ("from django.urls import path\n"
                        f"from {app_name}.urls import *\n"
                        f"from {app_name}.models import *\n"
                        f"urlpatterns = [\n\n"
                        f"]")
    with open(os.path.join(app_name, 'urls.py'), 'w') as file:
        file.write(urls_file_content)
    print("Urls.py in app is changed")

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
    print("Urls.py in project is changed")
    setting_by_path = os.path.join(project_name, 'settings.py')

    with open(setting_by_path) as file:
        content = file.read()
        pattern = re.compile("'django.contrib.staticfiles',\n", re.DOTALL)
        new_string = ("'django.contrib.staticfiles',\n"
                      f"\t'{app_name}',\n")
        content = pattern.sub(new_string, content)

    with open(setting_by_path, 'w') as file:
        file.write(content)
    print("Settings.py is changed")