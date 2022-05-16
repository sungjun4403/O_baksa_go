from distutils.debug import DEBUG
from email.mime import base
from importlib.resources import path
import re
from django.shortcuts import redirect, render
from django.conf import settings
from .models import *
from plotly import *
from matplotlib  import *
import networkx as nx
import osmnx as ox
import requests
import matplotlib
import matplotlib.pyplot as plt
from plotly.offline import plot
import time
import sys
import os
from geopy.geocoders import Nominatim
import googlemaps
from django.utils import timezone
from PIL import Image
from io import BytesIO
import base64
import mimetypes
import mpld3
import pandas as pd
import json
import datetime

matplotlib.use('Agg')

# Create your views here.
def home (request):
    return render(request, 'home.html')

def input (request):
    return render(request, 'input.html')

def get_options(request):
    ifsame = request.POST.get('ifsame')
    Destination = request.POST.get('Destination')
    #Starting_Point, 참고항목은 안받음
    POST_CODE = request.POST.get('SP_postcode')      #일단은 unnecessary 해보임 
    ADDRESS = request.POST.get('SP_address')        #지번 주소이거나 우편주소이거나 
    DETAILED_ADDRESS = request.POST.get('SP_deatilAddress')   
    ETC = request.POST.get('SP_extraaddress')        ##일단은 unnecessary 해보임 

    Max_Length = request.POST.get('Max_Length')

    Starting_Point = str(POST_CODE) + " " +  str(ADDRESS) + " " + str(DETAILED_ADDRESS) + " " + str(ETC)

    print(ifsame)
    print(Destination)
    print(Starting_Point)

    try:  
        if str(Max_Length).strip() == "" :      #아무값도 안들어왔을때 
            pass
        else:
            Max_Length = int(Max_Length)        

    except:
        return redirect('input')        #숫자가 아닐떄

    if ifsame == '1':
        Destination = Starting_Point    #출발지 = 목적지 일떄
    
    if str(Max_Length).strip() == "" :      #아무값도 안들어왔을때 
        Max_Length = 100000

    if str(Destination).strip() == "" and ifsame == "0" :     #위에서 안걸렸는데 값이 안들어왔을떄
        return redirect ('input')
    if str(Starting_Point).strip() == "" :      #시작점이 안들어왔을 떄
        return redirect ('input')

    SPL = google_geocode(str(ADDRESS))

    get_map(ifsame, SPL, 'DL', Max_Length)

    return render(request, 'show_options.html')


def get_map (ifsame, SPL, DL, Max_Length):      #Starting_Point_List, Destination_List / each list contains 'formatted_addres', 'location', 'address_type'
    
    import sys,os
    sys.path.append(os.path.realpath('..'))
    start = time.time() 
    
    ox.config(use_cache = True, log_console = True)
    ox.__version__

    G = ox.graph_from_address (SPL[0], network_type = 'drive_service')        #get 이니까 저기 성남시 경기도 지역 부분을 변수로 
    ox.plot_graph(G, node_size = 0.5, node_color = 'blue')
    plt.savefig("graphimage.png", format="PNG")

    end = time.time()       #프로세스 소요 시간 
    process_time = round(end - start, 4)
    
    print()
    print("===========================")
    print(str(process_time) + " sec")
    print("===========================")
    print()

    
def google_geocode (got_place):
    gmaps = googlemaps.Client(key = 'AIzaSyAawgC_tb1v8ro5BYuGs7BbhcuqYfI26ws')
    got_geocode = gmaps.geocode(got_place)
    print(got_geocode)
    lst = got_geocode
    llst = []       #[0] : location x, y / [1] : formatted_address / [2] : address_type 
    loc_to_append = str(lst[0].get('geometry').get('location').get('lat'))
    loc_to_append = loc_to_append + ", " + str(lst[0].get('geometry').get('location').get('lng'))
    llst.append(loc_to_append)
    llst.append(lst[0].get('formatted_address'))
    llst.append(lst[0].get('types')[0])
    print(llst)
    return llst


def get_cvs (got_place):
    # gmaps = googlemaps.

    return None


def end(request):
    return render (request, 'end.html')
