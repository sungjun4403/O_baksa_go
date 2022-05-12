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
matplotlib.use('Agg')
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

# Create your views here.
def home (request):
    return render(request, 'home.html')

def input (request):
    return render(request, 'input.html')

def get_options(request):
    ifsame = request.POST.get('ifsame')
    Destination = request.POST.get('Destination')
    Starting_Point = request.POST.get('Starting_Point')
    Max_Length = request.POST.get('Max_Length')

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

    print(ifsame + " / " + Destination + " / " + Starting_Point + " / " + str(Max_Length))

    get_map(ifsame, google_geocode(Starting_Point), Destination, Max_Length)

    path = '/Users/sungjun/Documents/O_baksa_go/OBSpjct/my_plot.png'

    
    return render(request, 'show_options.html', {'ifsame' : ifsame, 'Destination' : Destination, 'Starting_Point' : Starting_Point, 'Max_Length' : Max_Length, })


def end(request):
    return render (request, 'end.html')

def get_map (ifsame, Starting_Point, Destination, Max_Length):
    
    import sys,os
    sys.path.append(os.path.realpath('..'))
    start = time.time() 
    
    ox.config(use_cache = True, log_console = True)
    ox.__version__

    # try:
    G = ox.graph_from_place (Starting_Point, network_type = 'drive_service')        #get 이니까 저기 성남시 경기도 지역 부분을 변수로 
    ox.plot_graph(G, node_size = 0.5, node_color = 'blue')
    plt.savefig("graphimage.png", format="PNG")
    # except:
    #     G1 = ox.graph_from_place(Starting_Point, network_type = 'drive_service')
    #     ox.plot_graph(G1, node_size = 0.5, node_color = 'blue')
    #     plt.savefig("graphimage.png", format="PNG")

    end = time.time()       #프로세스 소요 시간 
    process_time = round(end - start, 4)
    
    print()
    print("===========================")
    print(str(process_time) + " sec")
    print("===========================")
    print()

def show_map (request):
    return render (request, 'show_map.html')

def google_geocode (got_place):
    gmaps = googlemaps.Client(key = 'AIzaSyAawgC_tb1v8ro5BYuGs7BbhcuqYfI26ws')
    got_geocode = gmaps.geocode(got_place, language='ko')
    got_geocode = str(got_geocode[0].get('formatted_address'))      #대한민국 분당구 서현동으로 리턴 
    got_geocode = got_geocode.strip()
    return got_geocode