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
    Starting_Point = request.POST.get('Starting_Point')
    Max_Length = request.POST.get('Max_Length')
    ifMT1 = request.POST.get('MT1')
    ifCS2 = request.POST.get('CS2')
    #0 : postcode / 1 : address / 2 : detailAddress / 3 : extraAddress
    Starting_Point_list = Starting_Point.split(" / ")
    Destination_Point_list = Destination.split(" / ")
    for p in range (0, len(Starting_Point_list)-1): Starting_Point_list[p] = str(Starting_Point_list[p]).strip()
    for q in range (0, len(Destination_Point_list)-1): Destination_Point_list[q] = str(Destination_Point_list[q]).strip()

    ADDRESS = Starting_Point_list[1]        
    address = Destination_Point_list[1]       

    try:  
        if str(Max_Length).strip() == "" :      #아무값도 안들어왔을때 
            pass
        else:
            Max_Length = int(Max_Length)        

    except:
        return redirect('input')        #숫자가 아닐떄
    
    if str(Max_Length).strip() == "" :      #아무값도 안들어왔을때 
        Max_Length = 5000

    #받을떄 좌표로 받으면 geocoding 스킵하는 로직 
    #SPL, DPL / 0 : location (lat, lng) / 1 : address / 2 : address_type
    SPL = [None] * 3        
    ADS = ADDRESS
    try:
        int(ADDRESS[5:9])
        SPLformat = "loc"
        ADDRESS = ADS
    except:
        SPLformat = "notloc"

    if SPLformat == "loc":
        SPL[0] = ADDRESS
        SPL[2] = 'location'
        print(str(SPL[0][:10]) + " " + str(SPL[0][12:])) 
        print("=================")
        print("location")
        print("=================")
    else:
        SPL = google_geocode(str(ADDRESS))
    
    DPL = [None] * 3
    ads = address
    try:
        int(address[5:9])
        DPLformat = "loc"
        address = ads
    except:
        DPLformat = "notloc"

    if DPLformat == "loc":
        DPL[0] = address
        DPL[2] = 'location'
        print(str(DPL[0][:10]) + " " + str(DPL[0][12:])) 
        print("=================")
        print("location")
        print("=================")
    else:
        DPL = google_geocode(str(address))
    
    
    #주변 편의점, 마트 
    if ifCS2 == "True": 
        CS2 = search_CS2(SPL, DPL, ifsame, Max_Length)
        CS2L = getlst(CS2)
    else: 
        CS2 = []
        CS2L = []
    if ifMT1 == "True": 
        MT1 = search_MT1(SPL, DPL, ifsame, Max_Length)
        MT1L = getlst(MT1)
    else: 
        MT1 = []
        MT1L = []
    print(SPL)
    print(DPL)
    
    get_map(ifsame, SPL, DPL, Max_Length, CS2L, MT1L)
    time.sleep(0.1)
    os.system("python manage.py collectstatic --no-input")
    print("**********************************************************************************************************************************************************************")
    return render(request, 'show_options.html', {'CS2' : CS2, 'lenCS2' : len(CS2), 'MT1' : MT1, 'lenMT1' : len(MT1), 'Max_Length' : Max_Length, 'ifMT1' : ifMT1, 'ifCS2' : ifCS2}) 


def end(request):
    return render (request, 'end.html')


def search_CS2(SPL, DPL, ifsame, Max_Length):        #MT1, CS2, 
    loc = SPL[0].split(", ")
    rest_api_key = '39b09cd965f4787143f206403f3f370b'
    header = {'Authorization': 'KakaoAK ' + rest_api_key}
    params = {
        'x' : float(loc[1]), 
        'y' : float(loc[0]),
        'radius' : int(Max_Length), 
        'page' : 10,      #tochange
        'size' : 15,
        'sort' : 'distance', 
        } 
    keywords = '편의점'
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(keywords)
    places = requests.get(url, headers=header, params=params).json()
    places = places.get('documents')
    lst = []
    # 0 : address_name / 1 : category_group_code / 2 : category_group_name / 3 : category_name / 4 : distance / 5 : id / 6 : phone / 7 : place_name / 8 : place_url / 9 : road_address_name / 10 : x / 11 : y
    for i in places:
        if i.get('category_group_code') == "CS2":
            to_append_list = []
            to_append_list.append(i.get('address_name'))
            to_append_list.append(i.get('category_group_code'))
            to_append_list.append(i.get('category_group_name'))
            to_append_list.append(i.get('category_name'))
            to_append_list.append(i.get('distance'))
            to_append_list.append(i.get('id'))
            to_append_list.append(i.get('phone'))
            to_append_list.append(i.get('place_name'))
            to_append_list.append(i.get('place_url'))
            to_append_list.append(i.get('road_address_name'))
            to_append_list.append(i.get('x'))
            to_append_list.append(i.get('y'))
            lst.append(to_append_list)
        else: pass
    return lst


def search_MT1(SPL, DPL, ifsame, Max_Length):        #MT1, CS2, 
    loc = SPL[0].split(", ")
    rest_api_key = '39b09cd965f4787143f206403f3f370b'
    header = {'Authorization': 'KakaoAK ' + rest_api_key}
    params = {
        'x' : float(loc[1]), 
        'y' : float(loc[0]),
        'radius' : int(Max_Length), 
        'page' : 10,      #tochange
        'size' : 15,
        'sort' : 'distance', 
        } 
    keywords = '마트'
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query={}'.format(keywords)
    places = requests.get(url, headers=header, params=params).json()
    places = places.get('documents')
    lst = []
    # 0 : address_name / 1 : category_group_code / 2 : category_group_name / 3 : category_name / 4 : distance / 5 : id / 6 : phone / 7 : place_name / 8 : place_url / 9 : road_address_name / 10 : x / 11 : y
    for i in places:
        if i.get('category_group_code') == "CS2": pass
        else:
            to_append_list = []
            to_append_list.append(i.get('address_name'))
            to_append_list.append(i.get('category_group_code'))
            to_append_list.append(i.get('category_group_name'))
            to_append_list.append(i.get('category_name'))
            to_append_list.append(i.get('distance'))
            to_append_list.append(i.get('id'))
            to_append_list.append(i.get('phone'))
            to_append_list.append(i.get('place_name'))
            to_append_list.append(i.get('place_url'))
            to_append_list.append(i.get('road_address_name'))
            to_append_list.append(i.get('x'))
            to_append_list.append(i.get('y'))
            lst.append(to_append_list)
        
    return lst


def getlst (places):
    lst = []
    for place in places:
        to_append_lst = [] 
        to_append_lst.append(place[10])
        to_append_lst.append(place[11])
        lst.append(to_append_lst)
    
    return lst


def google_geocode (got_place):
    gmaps = googlemaps.Client(key = 'AIzaSyAawgC_tb1v8ro5BYuGs7BbhcuqYfI26ws')
    got_geocode = gmaps.geocode((got_place), language='ko')
    lst = got_geocode
    llst = []       #[0] : location x, y / [1] : formatted_address / [2] : address_type 
    loc_to_append = str(lst[0].get('geometry').get('location').get('lat'))
    loc_to_append = loc_to_append + ", " + str(lst[0].get('geometry').get('location').get('lng'))
    llst.append(loc_to_append)
    llst.append(lst[0].get('formatted_address'))
    llst.append(lst[0].get('types')[0])
    return llst


def get_map (ifsame, SPL, DPL, Max_Length, CS2L, MT1L):      #Starting_Point_List, Destination_List / each list contains 'formatted_addres', 'location', 'address_type'
    
    sys.path.append(os.path.realpath('..'))
    start = time.time() 
    
    ox.config(use_cache = True, log_console = True)
    ox.__version__

    G = ox.graph_from_address (SPL[0], network_type = 'drive_service')        #get 이니까 저기 성남시 경기도 지역 부분을 변수로 

    spl = SPL[0].split(", ")
    spllat = float(str(spl[0]).strip())
    spllng = float(str(spl[1]).strip())
    orgn = ox.nearest_nodes(G, spllng, spllat)

    dpl = DPL[0].split(", ")
    dpllat = float(str(dpl[0]).strip())
    dpllng = float(str(dpl[1]).strip())
    dstn = ox.nearest_nodes(G, dpllng, dpllat)

    route = ox.shortest_path(G, orgn, dstn, weight = 'length')

    ox.plot_graph_route(G, route, orig_dest_size=1, show = False, save = True, filepath = "OBSpjct/static/graphimage.png", route_linewidth = 0)

    end = time.time()       #프로세스 소요 시간 
    process_time = round(end - start, 4)
    
    print()
    print("===========================")
    print(str(process_time) + " sec")
    print(orgn)
    print(dstn)
    print(route)
    print("===========================")
    print()



def forCS1(Max_Legnth):
    rslt = []
    prcs = []
    for p in range (0, Max_Legnth, 100):
        for src in search_CS2:
            prcs.append(src)
    for q in range(0, len(prcs), 1):
        if prcs[q] in rslt:
            pass
        else: rslt.append(prcs[q])
    return rslt 


def forMT1(Max_Length):
    rslt = []
    prcs = []
    for p in range (0, Max_Length, 100):
        for src in search_MT1:
            prcs.append(src)
    for q in range (0, len(prcs), 1):
        if prcs[q] in rslt:
            pass
        else: rslt.append(prcs[q])
    print(rslt)
    return rslt