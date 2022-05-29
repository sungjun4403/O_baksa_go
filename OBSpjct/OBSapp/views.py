from distutils.debug import DEBUG
from email.mime import base
from importlib.resources import path
from operator import indexOf, truediv
import re
from turtle import distance
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
import copy

matplotlib.use('Agg')
ox.config(use_cache = True, log_console = True)
ox.__version__
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
    if Starting_Point[-1] == ')'and Starting_Point[0] == '(':
        Starting_Point.strip()
        Starting_Point = Starting_Point[1:-1]
        Starting_Point = " / " + str(Starting_Point) + " / " + " / "
    if Destination[-1] == ')'and Destination[0] == '(':
        Destination.strip()
        Destination = Destination[1:-1]
        Destination = " / " + str(Destination) + " / " + " / "

    Starting_Point_list = Starting_Point.split(" / ")
    Destination_Point_list = Destination.split(" / ")
    for p in range (0, len(Starting_Point_list)-1): Starting_Point_list[p] = str(Starting_Point_list[p]).strip()
    for q in range (0, len(Destination_Point_list)-1): Destination_Point_list[q] = str(Destination_Point_list[q]).strip()

    ADDRESS = Starting_Point_list[1]        
    address = Destination_Point_list[1]       

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
    
    try:  
        if str(Max_Length).strip() == "" :      #아무값도 안들어왔을때 
            pass
        else:
            Max_Length = int(Max_Length)        

    except:
        return redirect('input')        #숫자가 아닐떄
    
    if str(Max_Length).strip() == "" :      #아무값도 안들어왔을때 
        Max_Length = 1000
    
    #주변 편의점, 마트 
    if ifCS2 == "True": 
        CS2 = forCS2(SPL, DPL, ifsame, Max_Length)
        CS2L = getlst(CS2)
    else: 
        CS2 = []
        CS2L = []
    if ifMT1 == "True": 
        MT1 = forMT1(SPL, DPL, ifsame, Max_Length)
        MT1L = getlst(MT1)
    else: 
        MT1 = []
        MT1L = []

    get_map(ifsame, SPL, DPL, Max_Length, CS2L, MT1L)
    time.sleep(0.1)
    os.system("python manage.py collectstatic --no-input")
    
    CS2str0 = lstTostr(CS2, 0)
    CS2str1 = lstTostr(CS2, 1)
    CS2str2 = lstTostr(CS2, 2)
    CS2str3 = lstTostr(CS2, 3)
    CS2str4 = lstTostr(CS2, 4)
    CS2str5 = lstTostr(CS2, 5)
    CS2str6 = lstTostr(CS2, 6)
    CS2str7 = lstTostr(CS2, 7)
    CS2str8 = lstTostr(CS2, 8)
    CS2str9 = lstTostr(CS2, 9)
    CS2str10 = lstTostr(CS2, 10)
    CS2str11 = lstTostr(CS2, 11)
    
    MT1str0 = lstTostr(MT1, 0)
    MT1str1 = lstTostr(MT1, 1)
    MT1str2 = lstTostr(MT1, 2)
    MT1str3 = lstTostr(MT1, 3)
    MT1str4 = lstTostr(MT1, 4)
    MT1str5 = lstTostr(MT1, 5)
    MT1str6 = lstTostr(MT1, 6)
    MT1str7 = lstTostr(MT1, 7)
    MT1str8 = lstTostr(MT1, 8)
    MT1str9 = lstTostr(MT1, 9)
    MT1str10 = lstTostr(MT1, 10)
    MT1str11 = lstTostr(MT1, 11)

    print("**********************************************************************************************************************************************************************")
    return render(request, 'show_options.html', {
        'CS2' : CS2, 'lenCS2' : len(CS2), 'MT1' : MT1, 'lenMT1' : len(MT1), 'Max_Length' : Max_Length, 'ifMT1' : ifMT1, 'ifCS2' : ifCS2, 'SPL' : SPL, 'DPL' : DPL, 
        'CS2str0' : CS2str0, 'CS2str1':CS2str1, 'CS2str2':CS2str2, 'CS2str3': CS2str3, 'CS2str4':CS2str4, 'CS2str5':CS2str5, 'CS2str6':CS2str6, 'CS2str7':CS2str7, 'CS2str8':CS2str8, 'CS2str9':CS2str9, 'CS2str10':CS2str10, 'CS2str11': CS2str11,
        'MT1str0':MT1str0, 'MT1str1':MT1str1, 'MT1str2':MT1str2, 'MT1str3':MT1str3, 'MT1str4':MT1str4, 'MT1str5':MT1str5, 'MT1str6':MT1str6, 'MT1str7':MT1str7, 'MT1str8':MT1str8, 'MT1str9':MT1str9, 'MT1str10':MT1str10, 'MT1str11':MT1str11
        }) 


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
        elif i.get('category_group_code') == "PS3": pass
        elif i.get('category_group_code') == "SC4": pass
        elif i.get('category_group_code') == "AC5": pass
        elif i.get('category_group_code') == "PK6": pass
        elif i.get('category_group_code') == "OL7": pass
        elif i.get('category_group_code') == "SW8": pass
        elif i.get('category_group_code') == "BK9": pass
        elif i.get('category_group_code') == "CT1": pass
        elif i.get('category_group_code') == "AG2": pass
        elif i.get('category_group_code') == "PO3": pass
        elif i.get('category_group_code') == "AT4": pass
        elif i.get('category_group_code') == "AD5": pass
        elif i.get('category_group_code') == "FD6": pass
        elif i.get('category_group_code') == "CE7": pass
        elif i.get('category_group_code') == "HP8": pass
        elif i.get('category_group_code') == "PM9": pass
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
        to_append_lst.append(place[11])
        to_append_lst.append(place[10])
        lst.append(to_append_lst)
    
    return lst


def lstTostr(lst, indx):
    rslt = []
    prcs = []
    for i in range(0, len(lst), 1):
         prcs.append(lst[i][indx])
    rslt = str(prcs)
    rslt = rslt[1:-1]
    return rslt


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
    start = time.time() 

    G = ox.graph_from_address (SPL[0], network_type = 'walk')        #get 이니까 저기 성남시 경기도 지역 부분을 변수로 

    spl = SPL[0].split(", ")
    spllat = float(str(spl[0]).strip())
    spllng = float(str(spl[1]).strip())
    orgn = ox.nearest_nodes(G, spllng, spllat)

    dpl = DPL[0].split(", ")
    dpllat = float(str(dpl[0]).strip())
    dpllng = float(str(dpl[1]).strip())
    dstn = ox.nearest_nodes(G, dpllng, dpllat)

    if len(CS2L) == 0:
        CS2L = [[]]
        CS2L[0].append(spllat)
        CS2L[0].append(spllng)
    if len(MT1L) == 0:
        MT1L = [[]]
        MT1L[0].append(dpllat)
        MT1L[0].append(dpllng)

    routes = []
    route = ox.shortest_path(G, orgn, dstn, weight = 'length')
    routes.append(route)
    routes.append([4686551530])
    routes.append([4339540676])
    routes.append([4634545557])

    length = nx.shortest_path_length(G=G, source=orgn, target=dstn, weight='length')

    gotlst = getNodelst(G, CS2L, MT1L)      #0 : CS2_nodes / 1 : MT1_nodes
    CS2_nodes = gotlst[0]
    MT1_nodes = gotlst[1]
    DFSsearch(G, CS2_nodes, MT1_nodes, orgn, dstn, Max_Length)
    


    if len(routes) == 1:
        ox.plot_graph_route(G, routes[0], orig_dest_size=100, show = False, save = True, filepath = "OBSpjct/static/graphimage.png", route_linewidth = 5, node_size = 8)
        graph_type = "route"
    elif len(route) == 0:
        ox.plot_graph(G, show = False, save = True, filepath = "OBSpjct/static/graphimage.png", node_size = 8)    
        graph_type = "not a route"
    else:
        ox.plot_graph_routes(G, routes, orig_dest_size=100, show = False, save = True, filepath = "OBSpjct/static/graphimage.png", route_linewidth = 5, node_size = 8)
        graph_type = "routes"
    

    end = time.time()       #프로세스 소요 시간 
    process_time = round(end - start, 4)
    
    

    print()
    print("===========================")
    print(str(process_time) + " sec")
    print(graph_type)
    print(orgn)
    print(dstn)
    print(CS2_nodes)
    print(MT1_nodes)
    print(route)
    print("===========================")
    print()


def forCS2(SPL, DPL, ifsame, Max_Length):
    rslt = []
    for p in range (0, int(Max_Length)+100, 100):
        src = search_CS2(SPL, DPL, ifsame,p)
        for q in range(0, len(src), 1):
            if src[q] not in rslt:
                rslt.append(src[q])
    return rslt


def forMT1(SPL, DPL, ifsame, Max_Length):
    rslt = []
    for p in range (0, int(Max_Length)+100, 100):
        src = search_MT1(SPL, DPL, ifsame, p)
        for q in range(0, len(src), 1):
            if src[q] not in rslt:
                rslt.append(src[q])
    return rslt


def DFSsearch(G, CS2_nodes, MT1_nodes, orgn, dstn, Max_Length):
    distance_from_SP = []
    to_sort = []
    routes = []
    total_distance = []     #routes와 1대1 대응 
    rslt = []       # 0 : shortest / 1 : many / 2 : neutral
    smlst = []

    #SPL부터 모든 편의점까지 거리 append(직선거리X, walk 실거리)
    for i in range(0, len(CS2_nodes), 1):
        to_append = 0
        to_append = nx.shortest_path_length(G=G, source=orgn, target=CS2_nodes[i], weight='length')
        distance_from_SP.append(to_append)
        to_sort.append(to_append)

    to_sort.sort()         

    for i in range(0, len(CS2_nodes), 1):     #factorial 1단계 
        CS2_nodes_c = copy.deepcopy(CS2_nodes)      #CS2_nodes deepcopy
        distnce = 0
        route = []      
        indx = distance_from_SP.index(to_sort[i])       #정렬된 순서가 가르키는 원래 거리
        a = CS2_nodes_c[indx]
        distnce += to_sort[i]
        route.append(orgn)
        route.append(a)
        CS2_nodes_c.remove(a)
        distance_from_SP.remove(distance_from_SP[indx])
        # new_distance = 
        print(route)
    return


def BFSsearch(G, CS2s, MT1s, orgn, dstn, Max_Length):

    return


def getNodelst(G, CS2L, MT1L):      #get nearest_nodes 
    rslt = []
    cs2nodes = []
    mt1nodes = [] 
    cs2lat = []
    cs2lng = []
    mt1lng = []
    mt1lat = []

    for p in range(0, len(CS2L), 1):
        cs2lat.append(float(CS2L[p][0]))
        cs2lng.append(float(CS2L[p][1]))
    cs2nodes = ox.nearest_nodes(G, cs2lng, cs2lat)
    
    for q in range(0, len(MT1L), 1):
        mt1lat.append(float(CS2L[q][0]))
        mt1lng.append(float(CS2L[q][1]))
        mt1nodes.append(ox.nearest_nodes(G, mt1lng, mt1lat))
    mt1nodes = ox.nearest_nodes(G, mt1lng, mt1lat)

    rslt.append(cs2nodes)
    rslt.append(mt1nodes)
    return rslt 
