from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from .utils import get_last_update
from pathlib import Path
import json,os

os.chdir(Path(__file__).parent.parent)
# Create your views here.
def homepage(request):
    return render(request,Path("wcresults","index.html"),{})

def return_hello_world(request,date_data):
    print(date_data)
    try:
        date_queried = datetime.strptime(date_data,"%Y%m%d")
    except ValueError:
        pass
    else:
        wc_data = list()
        wc_data_result = list()
        with open(Path("result","scrapper_result","WCresults.json")) as f:
            wc_data = json.load(f)
        for match_data in wc_data:
            if date_queried.strftime("%y-%m-%d") in match_data["match_time"]:
                wc_data_result.append(match_data)
        return JsonResponse({"date_data":date_data,"data":wc_data_result,"last_update":get_last_update()})
    return JsonResponse({"date_data":date_data,"data":"internal error"}) 