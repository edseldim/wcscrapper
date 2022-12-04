import os, json, subprocess

with open("./config.json","r") as f:
    env_variables = json.load(f)
    for key, value in env_variables.items():
        os.environ[key] = value

subprocess.Popen(["python","web_scrapping\scheduler_main.py"],shell=True)
subprocess.Popen(["python","django_wcapp\django_wcapp\manage.py","runserver"],shell=True)