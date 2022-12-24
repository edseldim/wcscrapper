import os, json, subprocess
from pathlib import Path

my_env = os.environ.copy()
try:
    with open("./config.json","r") as f:
        env_variables = json.load(f)
        for key, value in env_variables.items():
            my_env[key] = value

except FileNotFoundError:
    print("config.json file was not found. Default configuration will be applied...")

my_env["python_executable"] = my_env.get("python_executable") or "python"
my_env["django_server_address_port"] = my_env.get("django_server_address_port") or "localhost:8000"
my_env["django_key"] = my_env.get("django_key") or "DJANGO-INSECURE-KEY"
my_env["webdriver_location"] = my_env.get("webdriver_location") or "web_scrapping/chromedriver.exe"
my_env["scrapper_exec_time"] = my_env.get("scrapper_exec_time") or "60"

subprocess.Popen([my_env["python_executable"],Path("web_scrapping","scheduler_main.py")])
subprocess.Popen([my_env["python_executable"],Path("django_wcapp","django_wcapp","manage.py"),"runserver",my_env["django_server_address_port"]])