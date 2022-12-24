import os,schedule, subprocess, time, json
from pathlib import Path
from datetime import datetime

def call_scrapper():
    print("Scrapper executed on "+str(time.now()))
    subprocess.run(["python", Path("web_scrapping","scrapper_main.py")])

def move_result():
    for file_obj in Path("./web_scrapping/").iterdir():
        if file_obj.name.lower() == "wcresults.json":
            with open(Path("django_wcapp","django_wcapp","result","scrapper_result","WCresults.json"),"w") as f:
                new_json = json.loads(file_obj.read_text()) # read the file before this with statement and pass it to the json.load
                json.dump(new_json,fp=f)
            print("file written on",datetime.fromtimestamp(file_obj.stat().st_mtime))

def wipe_results():
    for file_path in ["web_scrapping/WCresults.html","web_scrapping/WCresults.json"]:
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass

scrapper_exec_time = int(os.environ.setdefault("scrapper_exec_time","30"))
schedule.every(scrapper_exec_time).minutes.do(call_scrapper)
schedule.every(scrapper_exec_time).minutes.do(move_result)
schedule.every(scrapper_exec_time).minutes.do(wipe_results)
while True:
    schedule.run_pending()
    time.sleep(30)