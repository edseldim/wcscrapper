from pathlib import Path
from datetime import datetime

def get_last_update(filepath = "./result/scrapper_result/"):
    files = [datetime.fromtimestamp(file_obj.stat().st_mtime) for file_obj in Path(filepath).iterdir() if file_obj.name.lower() == "wcresults.json"]
    return files[0]

if __name__ == "__main__":
    print(get_last_update())